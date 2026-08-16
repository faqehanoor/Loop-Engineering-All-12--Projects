import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import scheduled_task
import periodic_loop


class TestScheduledTask(unittest.TestCase):
    """Tests for the scheduled_task module."""

    @patch("scheduled_task.time.sleep")
    def test_run_success(self, mock_sleep):
        with patch("scheduled_task.random.random", return_value=0.8):
            result = scheduled_task.run()
        self.assertEqual(result["status"], "ok")
        self.assertIn("message", result)
        self.assertIn("timestamp", result)

    @patch("scheduled_task.time.sleep")
    def test_run_failure(self, mock_sleep):
        with patch("scheduled_task.random.random", return_value=0.1):
            with self.assertRaises(RuntimeError):
                scheduled_task.run()


class TestPeriodicLoopAllSuccess(unittest.TestCase):
    """Tests for periodic_loop when all runs succeed."""

    @patch("periodic_loop.time.sleep")
    @patch("periodic_loop.run")
    def test_all_runs_succeed(self, mock_run, mock_sleep):
        mock_run.return_value = {"status": "ok", "message": "done"}
        original_max = periodic_loop.MAX_RUNS
        periodic_loop.MAX_RUNS = 3
        try:
            summary = periodic_loop.periodic_loop()
        finally:
            periodic_loop.MAX_RUNS = original_max

        self.assertEqual(summary["success_count"], 3)
        self.assertEqual(summary["fail_count"], 0)
        self.assertEqual(len(summary["history"]), 3)
        for entry in summary["history"]:
            self.assertEqual(entry["status"], "ok")


class TestPeriodicLoopAllFail(unittest.TestCase):
    """Tests for periodic_loop when all runs fail."""

    @patch("periodic_loop.time.sleep")
    @patch("periodic_loop.run", side_effect=RuntimeError("boom"))
    def test_all_runs_fail(self, mock_run, mock_sleep):
        original_max = periodic_loop.MAX_RUNS
        periodic_loop.MAX_RUNS = 3
        try:
            summary = periodic_loop.periodic_loop()
        finally:
            periodic_loop.MAX_RUNS = original_max

        self.assertEqual(summary["success_count"], 0)
        self.assertEqual(summary["fail_count"], 3)
        self.assertEqual(len(summary["history"]), 3)
        for entry in summary["history"]:
            self.assertEqual(entry["status"], "error")


class TestPeriodicLoopMixed(unittest.TestCase):
    """Tests for periodic_loop with mixed success/failure."""

    @patch("periodic_loop.time.sleep")
    @patch("periodic_loop.run")
    def test_mixed_results(self, mock_run, mock_sleep):
        mock_run.side_effect = [
            {"status": "ok", "message": "done"},
            RuntimeError("fail"),
            {"status": "ok", "message": "done"},
        ]
        original_max = periodic_loop.MAX_RUNS
        periodic_loop.MAX_RUNS = 3
        try:
            summary = periodic_loop.periodic_loop()
        finally:
            periodic_loop.MAX_RUNS = original_max

        self.assertEqual(summary["success_count"], 2)
        self.assertEqual(summary["fail_count"], 1)
        self.assertEqual(summary["history"][0]["status"], "ok")
        self.assertEqual(summary["history"][1]["status"], "error")
        self.assertEqual(summary["history"][2]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
