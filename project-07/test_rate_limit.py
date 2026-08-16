import os
import sys
import time
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))

import api_service
import rate_limiter


class TestApiService(unittest.TestCase):
    """Test the simulated API service."""

    @patch("api_service.random.random", return_value=0.3)
    @patch("api_service.random.randint", return_value=42)
    def test_call_success(self, mock_randint, mock_random):
        result = api_service.call()
        self.assertEqual(result["status"], "ok")

    @patch("api_service.random.random", return_value=0.7)
    def test_call_rate_limited(self, mock_random):
        with self.assertRaises(ConnectionError):
            api_service.call()

    @patch("api_service.random.random", return_value=0.9)
    def test_call_server_error(self, mock_random):
        with self.assertRaises(RuntimeError):
            api_service.call()


class TestTokenBucketInit(unittest.TestCase):
    """Test token bucket initialization."""

    def test_starts_full(self):
        bucket = rate_limiter.TokenBucket(rate=3, capacity=5)
        self.assertEqual(bucket.tokens, 5)

    def test_custom_capacity(self):
        bucket = rate_limiter.TokenBucket(rate=1, capacity=10)
        self.assertEqual(bucket.tokens, 10)


class TestTokenBucketConsume(unittest.TestCase):
    """Test token consumption and throttling."""

    @patch("rate_limiter.time.time", return_value=100)
    def test_consume_when_tokens_available(self, mock_time):
        bucket = rate_limiter.TokenBucket(rate=3, capacity=5)
        self.assertTrue(bucket.consume())
        self.assertEqual(bucket.tokens, 4)

    @patch("rate_limiter.time.time", return_value=100)
    def test_consume_throttles_when_empty(self, mock_time):
        bucket = rate_limiter.TokenBucket(rate=1, capacity=1)
        bucket.consume()
        self.assertFalse(bucket.consume())

    @patch("rate_limiter.time.time", return_value=100)
    def test_refill_adds_tokens(self, mock_time):
        bucket = rate_limiter.TokenBucket(rate=3, capacity=5)
        bucket.consume()
        bucket.consume()
        self.assertEqual(bucket.tokens, 3)

        mock_time.return_value = 102
        self.assertTrue(bucket.consume())
        self.assertAlmostEqual(bucket.tokens, 4.0, places=1)

    @patch("rate_limiter.time.time", return_value=100)
    def test_refill_caps_at_capacity(self, mock_time):
        bucket = rate_limiter.TokenBucket(rate=3, capacity=5)
        mock_time.return_value = 200
        bucket.consume()
        self.assertEqual(bucket.tokens, 4)

    @patch("rate_limiter.time.time", return_value=100)
    def test_history_recorded(self, mock_time):
        bucket = rate_limiter.TokenBucket(rate=3, capacity=1)
        bucket.consume()
        bucket.consume()
        self.assertEqual(len(bucket.history), 2)
        self.assertEqual(bucket.history[0]["event"], "consumed")
        self.assertEqual(bucket.history[1]["event"], "throttled")


class TestRateLimitLoop(unittest.TestCase):
    """Test the full rate limiting loop."""

    @patch("rate_limiter.time.sleep")
    @patch("rate_limiter.time.time")
    @patch("rate_limiter.call")
    def test_all_succeed_when_enough_tokens(self, mock_call, mock_time, mock_sleep):
        original_max = rate_limiter.MAX_CALLS
        original_rate = rate_limiter.RATE_LIMIT
        try:
            rate_limiter.MAX_CALLS = 3
            rate_limiter.RATE_LIMIT = 100
            mock_time.return_value = 100
            mock_call.return_value = {"status": "ok", "message": "success"}
            summary = rate_limiter.rate_limit_loop()
            self.assertEqual(summary["succeeded"], 3)
            self.assertEqual(summary["throttled"], 0)
        finally:
            rate_limiter.MAX_CALLS = original_max
            rate_limiter.RATE_LIMIT = original_rate

    @patch("rate_limiter.time.sleep")
    @patch("rate_limiter.time.time")
    @patch("rate_limiter.call")
    def test_throttled_when_tokens_depleted(self, mock_call, mock_time, mock_sleep):
        original_max = rate_limiter.MAX_CALLS
        original_rate = rate_limiter.RATE_LIMIT
        try:
            rate_limiter.MAX_CALLS = 10
            rate_limiter.RATE_LIMIT = 2
            mock_time.return_value = 100
            mock_call.return_value = {"status": "ok", "message": "success"}
            summary = rate_limiter.rate_limit_loop()
            self.assertGreater(summary["throttled"], 0)
            self.assertGreater(summary["succeeded"], 0)
        finally:
            rate_limiter.MAX_CALLS = original_max
            rate_limiter.RATE_LIMIT = original_rate

    @patch("rate_limiter.time.sleep")
    @patch("rate_limiter.time.time")
    @patch("rate_limiter.call", side_effect=RuntimeError("server error"))
    def test_server_errors_counted(self, mock_call, mock_time, mock_sleep):
        original_max = rate_limiter.MAX_CALLS
        original_rate = rate_limiter.RATE_LIMIT
        try:
            rate_limiter.MAX_CALLS = 3
            rate_limiter.RATE_LIMIT = 100
            mock_time.return_value = 100
            summary = rate_limiter.rate_limit_loop()
            self.assertEqual(summary["succeeded"], 0)
            self.assertEqual(summary["failed"], 3)
            self.assertEqual(summary["throttled"], 0)
        finally:
            rate_limiter.MAX_CALLS = original_max
            rate_limiter.RATE_LIMIT = original_rate


if __name__ == "__main__":
    unittest.main()
