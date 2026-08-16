import unittest
from unittest.mock import patch, MagicMock
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import flaky_task
import retry_loop


class TestFlakyTask(unittest.TestCase):
    """Tests for the flaky_task module."""

    @patch("flaky_task.time.sleep")
    @patch("flaky_task.random.random", return_value=0.8)
    def test_run_success(self, mock_random, mock_sleep):
        result = flaky_task.run()
        self.assertTrue(result)

    @patch("flaky_task.time.sleep")
    @patch("flaky_task.random.random", return_value=0.2)
    def test_run_failure(self, mock_random, mock_sleep):
        with self.assertRaises(RuntimeError):
            flaky_task.run()


class TestRetryLoopSuccess(unittest.TestCase):
    """Tests for retry_loop when the task eventually succeeds."""

    @patch("retry_loop.time.sleep")
    @patch("retry_loop.run", return_value=True)
    def test_succeeds_on_first_attempt(self, mock_run, mock_sleep):
        result = retry_loop.retry_with_timeout()
        self.assertTrue(result)
        self.assertEqual(mock_run.call_count, 1)

    @patch("retry_loop.time.sleep")
    @patch("retry_loop.run", side_effect=[RuntimeError, RuntimeError, True])
    def test_succeeds_after_retries(self, mock_run, mock_sleep):
        result = retry_loop.retry_with_timeout()
        self.assertTrue(result)
        self.assertEqual(mock_run.call_count, 3)


class TestRetryLoopFailure(unittest.TestCase):
    """Tests for retry_loop when all attempts fail."""

    @patch("retry_loop.time.sleep")
    @patch("retry_loop.run", side_effect=RuntimeError)
    def test_all_attempts_fail(self, mock_run, mock_sleep):
        result = retry_loop.retry_with_timeout()
        self.assertFalse(result)
        self.assertEqual(mock_run.call_count, retry_loop.MAX_RETRIES)


class TestRetryLoopTimeout(unittest.TestCase):
    """Tests for retry_loop timeout behavior."""

    @patch("retry_loop.time.time")
    @patch("retry_loop.time.sleep")
    @patch("retry_loop.run", side_effect=RuntimeError)
    def test_timeout_stops_retries(self, mock_run, mock_sleep, mock_time):
        mock_time.side_effect = [0, 0, 31]
        result = retry_loop.retry_with_timeout()
        self.assertFalse(result)
        self.assertLess(mock_run.call_count, retry_loop.MAX_RETRIES)


if __name__ == "__main__":
    unittest.main()
