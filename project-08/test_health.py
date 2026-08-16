import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))

import health_service
import health_monitor


class TestHealthService(unittest.TestCase):
    """Tests for the health_service module."""

    @patch("health_service.random.random", return_value=0.3)
    @patch("health_service.random.uniform", return_value=0.05)
    def test_check_healthy(self, mock_uniform, mock_random):
        result = health_service.check()
        self.assertEqual(result["status"], "healthy")

    @patch("health_service.random.random", return_value=0.7)
    @patch("health_service.random.uniform", return_value=1.5)
    def test_check_degraded(self, mock_uniform, mock_random):
        result = health_service.check()
        self.assertEqual(result["status"], "degraded")

    @patch("health_service.random.random", return_value=0.95)
    def test_check_unreachable(self, mock_random):
        with self.assertRaises(ConnectionError):
            health_service.check()

    @patch("health_service.random.random", return_value=0.3)
    def test_recover_success(self, mock_random):
        result = health_service.recover()
        self.assertEqual(result["status"], "recovered")

    @patch("health_service.random.random", return_value=0.9)
    def test_recover_failure(self, mock_random):
        result = health_service.recover()
        self.assertEqual(result["status"], "failed")


class TestHealthMonitorInit(unittest.TestCase):
    """Tests for HealthMonitor initialization."""

    def test_starts_healthy(self):
        monitor = health_monitor.HealthMonitor()
        self.assertEqual(monitor.state, health_monitor.HEALTHY)

    def test_custom_thresholds(self):
        monitor = health_monitor.HealthMonitor(failure_threshold=5, recovery_threshold=3)
        self.assertEqual(monitor.failure_threshold, 5)
        self.assertEqual(monitor.recovery_threshold, 3)


class TestHealthMonitorHealthy(unittest.TestCase):
    """Tests for healthy state behavior."""

    @patch("health_monitor.check")
    def test_stays_healthy_on_success(self, mock_check):
        mock_check.return_value = {"status": "healthy", "response_time": 0.05, "message": "ok"}
        monitor = health_monitor.HealthMonitor()
        result = monitor.check_health()
        self.assertEqual(result["state"], health_monitor.HEALTHY)
        self.assertTrue(result["success"])

    @patch("health_monitor.check")
    def test_records_ok_event(self, mock_check):
        mock_check.return_value = {"status": "healthy", "response_time": 0.05, "message": "ok"}
        monitor = health_monitor.HealthMonitor()
        monitor.check_health()
        self.assertEqual(monitor.history[-1]["event"], "ok")


class TestHealthMonitorDegraded(unittest.TestCase):
    """Tests for degraded state transitions."""

    @patch("health_monitor.check")
    def test_transitions_to_degraded(self, mock_check):
        mock_check.return_value = {"status": "degraded", "response_time": 2.0, "message": "slow"}
        monitor = health_monitor.HealthMonitor()
        result = monitor.check_health()
        self.assertEqual(result["state"], health_monitor.DEGRADED)

    @patch("health_monitor.check")
    def test_stays_degraded(self, mock_check):
        mock_check.return_value = {"status": "degraded", "response_time": 2.0, "message": "slow"}
        monitor = health_monitor.HealthMonitor()
        monitor.check_health()
        monitor.check_health()
        self.assertEqual(monitor.history[-1]["event"], "still_degraded")


class TestHealthMonitorUnhealthy(unittest.TestCase):
    """Tests for unhealthy state and recovery triggering."""

    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_transitions_to_unhealthy_at_threshold(self, mock_check, mock_recover):
        mock_recover.return_value = {"status": "recovered", "message": "ok"}
        monitor = health_monitor.HealthMonitor(failure_threshold=2)
        monitor.check_health()
        result = monitor.check_health()
        self.assertEqual(result["state"], health_monitor.UNHEALTHY)

    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_recovery_triggered(self, mock_check, mock_recover):
        mock_recover.return_value = {"status": "recovered", "message": "ok"}
        monitor = health_monitor.HealthMonitor(failure_threshold=2)
        monitor.check_health()
        monitor.check_health()
        self.assertEqual(monitor.recovery_attempts, 1)

    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_stays_unhealthy_after_failed_recovery(self, mock_check, mock_recover):
        mock_recover.return_value = {"status": "failed", "message": "nope"}
        monitor = health_monitor.HealthMonitor(failure_threshold=2)
        monitor.check_health()
        monitor.check_health()
        monitor.check_health()
        self.assertEqual(monitor.state, health_monitor.UNHEALTHY)

    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_failure_count_resets_on_success(self, mock_check, mock_recover):
        mock_recover.return_value = {"status": "recovered", "message": "ok"}
        monitor = health_monitor.HealthMonitor(failure_threshold=3)
        monitor.check_health()
        monitor.check_health()
        self.assertEqual(monitor.failure_count, 2)
        mock_check.side_effect = None
        mock_check.return_value = {"status": "healthy", "response_time": 0.05, "message": "ok"}
        monitor.check_health()
        self.assertEqual(monitor.failure_count, 0)


class TestHealthMonitorRecovery(unittest.TestCase):
    """Tests for recovery from unhealthy/degraded back to healthy."""

    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_recovery_requires_consecutive_ok(self, mock_check, mock_recover):
        mock_recover.return_value = {"status": "recovered", "message": "ok"}
        monitor = health_monitor.HealthMonitor(failure_threshold=2, recovery_threshold=2)
        monitor.check_health()
        monitor.check_health()
        self.assertEqual(monitor.state, health_monitor.UNHEALTHY)
        mock_check.side_effect = None
        mock_check.return_value = {"status": "healthy", "response_time": 0.05, "message": "ok"}
        monitor.check_health()
        self.assertEqual(monitor.state, health_monitor.UNHEALTHY)
        self.assertEqual(monitor.history[-1]["event"], "improving")
        monitor.check_health()
        self.assertEqual(monitor.state, health_monitor.HEALTHY)

    @patch("health_monitor.check")
    def test_recovery_count_resets_on_failure(self, mock_check):
        monitor = health_monitor.HealthMonitor(failure_threshold=3, recovery_threshold=2)
        monitor.recovery_count = 1
        mock_check.side_effect = ConnectionError("down")
        monitor.check_health()
        self.assertEqual(monitor.recovery_count, 0)


class TestWatchdogLoop(unittest.TestCase):
    """Tests for the full watchdog loop."""

    @patch("health_monitor.time.sleep")
    @patch("health_monitor.time.time")
    @patch("health_monitor.check")
    def test_all_healthy(self, mock_check, mock_time, mock_sleep):
        original_max = health_monitor.MAX_CHECKS
        try:
            health_monitor.MAX_CHECKS = 3
            mock_check.return_value = {"status": "healthy", "response_time": 0.05, "message": "ok"}
            summary = health_monitor.watchdog_loop()
            self.assertEqual(summary["healthy_checks"], 3)
            self.assertEqual(summary["unhealthy_checks"], 0)
            self.assertEqual(summary["final_state"], health_monitor.HEALTHY)
        finally:
            health_monitor.MAX_CHECKS = original_max

    @patch("health_monitor.time.sleep")
    @patch("health_monitor.time.time")
    @patch("health_monitor.recover")
    @patch("health_monitor.check", side_effect=ConnectionError("down"))
    def test_all_unhealthy(self, mock_check, mock_recover, mock_time, mock_sleep):
        original_max = health_monitor.MAX_CHECKS
        try:
            health_monitor.MAX_CHECKS = 5
            mock_recover.return_value = {"status": "recovered", "message": "ok"}
            summary = health_monitor.watchdog_loop()
            self.assertGreater(summary["unhealthy_checks"], 0)
            self.assertGreater(summary["recovery_attempts"], 0)
        finally:
            health_monitor.MAX_CHECKS = original_max

    @patch("health_monitor.time.sleep")
    @patch("health_monitor.time.time")
    @patch("health_monitor.recover")
    @patch("health_monitor.check")
    def test_mixed_results(self, mock_check, mock_recover, mock_time, mock_sleep):
        original_max = health_monitor.MAX_CHECKS
        try:
            health_monitor.MAX_CHECKS = 5
            mock_recover.return_value = {"status": "recovered", "message": "ok"}
            mock_check.side_effect = [
                {"status": "healthy", "response_time": 0.05, "message": "ok"},
                ConnectionError("down"),
                ConnectionError("down"),
                ConnectionError("down"),
                {"status": "healthy", "response_time": 0.05, "message": "ok"},
            ]
            summary = health_monitor.watchdog_loop()
            self.assertGreater(summary["healthy_checks"], 0)
            self.assertGreater(summary["unhealthy_checks"], 0)
        finally:
            health_monitor.MAX_CHECKS = original_max


if __name__ == "__main__":
    unittest.main()
