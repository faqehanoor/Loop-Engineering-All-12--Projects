import unittest
from unittest.mock import patch
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import api_service
import circuit_breaker


class TestApiService(unittest.TestCase):
    """Tests for the api_service module."""

    @patch("api_service.time.sleep")
    @patch("api_service.random.random", return_value=0.8)
    def test_call_success(self, mock_random, mock_sleep):
        result = api_service.call()
        self.assertEqual(result["status"], "ok")
        self.assertIn("message", result)

    @patch("api_service.time.sleep")
    @patch("api_service.random.random", return_value=0.1)
    def test_call_failure(self, mock_random, mock_sleep):
        with self.assertRaises(ConnectionError):
            api_service.call()


class TestCircuitBreakerClosed(unittest.TestCase):
    """Tests for circuit breaker in CLOSED state."""

    def test_starts_closed(self):
        cb = circuit_breaker.CircuitBreaker()
        self.assertEqual(cb.state, circuit_breaker.CLOSED)
        self.assertEqual(cb.failure_count, 0)

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.call")
    def test_success_resets_count(self, mock_call, mock_sleep):
        mock_call.return_value = {"status": "ok", "message": "done"}
        cb = circuit_breaker.CircuitBreaker(failure_threshold=3)
        cb.failure_count = 2
        result = cb.call_service()
        self.assertTrue(result["success"])
        self.assertEqual(cb.failure_count, 0)
        self.assertEqual(cb.state, circuit_breaker.CLOSED)

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_failure_increments_count(self, mock_call, mock_sleep):
        cb = circuit_breaker.CircuitBreaker(failure_threshold=3)
        cb.call_service()
        self.assertEqual(cb.failure_count, 1)
        self.assertEqual(cb.state, circuit_breaker.CLOSED)


class TestCircuitBreakerTrips(unittest.TestCase):
    """Tests for circuit breaker tripping to OPEN state."""

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.time.time", return_value=100)
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_trips_at_threshold(self, mock_call, mock_time, mock_sleep):
        cb = circuit_breaker.CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.OPEN)
        self.assertEqual(cb.failure_count, 3)


class TestCircuitBreakerOpen(unittest.TestCase):
    """Tests for circuit breaker in OPEN state."""

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.time.time")
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_open_rejects_calls(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [100, 101]
        cb = circuit_breaker.CircuitBreaker(failure_threshold=2, cooldown=10)
        cb.call_service()
        cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.OPEN)
        result = cb.call_service()
        self.assertFalse(result["success"])
        self.assertEqual(result["state"], circuit_breaker.OPEN)
        self.assertIn("Circuit OPEN", result["message"])

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.time.time")
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_open_transitions_to_half_open(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [100, 111, 111]
        cb = circuit_breaker.CircuitBreaker(failure_threshold=2, cooldown=10)
        cb.call_service()
        cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.OPEN)
        result = cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.OPEN)


class TestCircuitBreakerHalfOpen(unittest.TestCase):
    """Tests for circuit breaker in HALF_OPEN state."""

    @patch("circuit_breaker.time.sleep")
    @patch("circuit_breaker.time.time")
    @patch("circuit_breaker.call")
    def test_half_open_success_closes(self, mock_call, mock_time, mock_sleep):
        mock_time.side_effect = [100, 111]
        mock_call.side_effect = [
            ConnectionError("fail"),
            ConnectionError("fail"),
            {"status": "ok", "message": "recovered"},
        ]
        cb = circuit_breaker.CircuitBreaker(failure_threshold=2, cooldown=10)
        cb.call_service()
        cb.call_service()
        result = cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.CLOSED)
        self.assertTrue(result["success"])

    @patch("circuit_breaker.time.time")
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_half_open_failure_reopens(self, mock_call, mock_time):
        mock_time.side_effect = [100, 111, 111]
        cb = circuit_breaker.CircuitBreaker(failure_threshold=2, cooldown=10)
        cb.call_service()
        cb.call_service()
        result = cb.call_service()
        self.assertEqual(cb.state, circuit_breaker.OPEN)
        self.assertFalse(result["success"])


class TestCircuitBreakerHistory(unittest.TestCase):
    """Tests for circuit breaker history tracking."""

    @patch("circuit_breaker.time.time", return_value=100)
    @patch("circuit_breaker.call", side_effect=ConnectionError("fail"))
    def test_history_records_events(self, mock_call, mock_time):
        cb = circuit_breaker.CircuitBreaker(failure_threshold=2)
        cb.call_service()
        cb.call_service()
        self.assertGreater(len(cb.history), 0)
        events = [h["event"] for h in cb.history]
        self.assertIn("tripped", events)


if __name__ == "__main__":
    unittest.main()
