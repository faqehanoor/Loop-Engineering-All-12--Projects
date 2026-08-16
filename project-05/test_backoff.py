import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import flaky_service
import backoff_loop


class TestFlakyService(unittest.TestCase):
    """Tests for the flaky_service module."""

    @patch("flaky_service.time.sleep")
    @patch("flaky_service.random.random", return_value=0.8)
    def test_call_success(self, mock_random, mock_sleep):
        result = flaky_service.call()
        self.assertEqual(result["status"], "ok")
        self.assertIn("message", result)

    @patch("flaky_service.time.sleep")
    @patch("flaky_service.random.random", return_value=0.1)
    def test_call_failure(self, mock_random, mock_sleep):
        with self.assertRaises(ConnectionError):
            flaky_service.call()


class TestBackoffWithJitter(unittest.TestCase):
    """Tests for the backoff_with_jitter function."""

    def test_jitter_returns_value_near_delay(self):
        delay = 4.0
        for _ in range(50):
            result = backoff_loop.backoff_with_jitter(delay)
            self.assertGreaterEqual(result, delay * (1 - backoff_loop.JITTER))
            self.assertLessEqual(result, delay * (1 + backoff_loop.JITTER))


class TestBackoffLoopSuccess(unittest.TestCase):
    """Tests for backoff_loop when the service eventually succeeds."""

    @patch("backoff_loop.time.sleep")
    @patch("backoff_loop.time.time", side_effect=[0, 0, 0, 1, 1, 1])
    @patch("backoff_loop.call", return_value={"status": "ok", "message": "done"})
    def test_succeeds_on_first_attempt(self, mock_call, mock_time, mock_sleep):
        result = backoff_loop.backoff_loop()
        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(len(result["delays"]), 0)

    @patch("backoff_loop.time.sleep")
    @patch("backoff_loop.time.time", side_effect=[0, 0, 0, 1, 1, 2, 2, 3])
    @patch("backoff_loop.call")
    def test_succeeds_after_retries(self, mock_call, mock_time, mock_sleep):
        mock_call.side_effect = [
            ConnectionError("fail"),
            ConnectionError("fail"),
            {"status": "ok", "message": "done"},
        ]
        result = backoff_loop.backoff_loop()
        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(len(result["delays"]), 2)


class TestBackoffLoopFailure(unittest.TestCase):
    """Tests for backoff_loop when all attempts fail."""

    @patch("backoff_loop.time.sleep")
    @patch("backoff_loop.time.time")
    @patch("backoff_loop.call", side_effect=ConnectionError("fail"))
    def test_all_attempts_fail(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [0] + [i * 2 for i in range(20)]
        result = backoff_loop.backoff_loop()
        self.assertFalse(result["success"])
        self.assertEqual(result["attempts"], backoff_loop.MAX_ATTEMPTS)


class TestBackoffLoopTimeout(unittest.TestCase):
    """Tests for backoff_loop timeout behavior."""

    @patch("backoff_loop.time.sleep")
    @patch("backoff_loop.time.time")
    @patch("backoff_loop.call", side_effect=ConnectionError("fail"))
    def test_timeout_stops_loop(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [0, 61]
        result = backoff_loop.backoff_loop()
        self.assertFalse(result["success"])
        self.assertLess(result["attempts"], backoff_loop.MAX_ATTEMPTS)


class TestBackoffDelays(unittest.TestCase):
    """Tests that backoff delays increase exponentially."""

    @patch("backoff_loop.time.sleep")
    @patch("backoff_loop.time.time")
    @patch("backoff_loop.call", side_effect=ConnectionError("fail"))
    def test_delays_increase(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [0] + [i for i in range(30)]
        result = backoff_loop.backoff_loop()
        self.assertFalse(result["success"])
        self.assertGreater(len(result["delays"]), 1)
        for i in range(1, len(result["delays"])):
            self.assertGreater(result["delays"][i], result["delays"][i - 1] * 0.5)


if __name__ == "__main__":
    unittest.main()
