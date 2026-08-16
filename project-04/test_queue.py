import unittest
from unittest.mock import patch, MagicMock, call
import queue
import sys
import os
import threading

sys.path.insert(0, os.path.dirname(__file__))

import work_item
import worker
import queue_loop


class TestWorkItem(unittest.TestCase):
    """Tests for the work_item module."""

    @patch("work_item.time.sleep")
    @patch("work_item.random.random", return_value=0.8)
    def test_process_success(self, mock_random, mock_sleep):
        item = {"id": 1, "data": "test"}
        result = work_item.process(item)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["id"], 1)
        self.assertIn("message", result)

    @patch("work_item.time.sleep")
    @patch("work_item.random.random", return_value=0.1)
    def test_process_failure(self, mock_random, mock_sleep):
        item = {"id": 2, "data": "test"}
        with self.assertRaises(RuntimeError):
            work_item.process(item)


class TestWorker(unittest.TestCase):
    """Tests for the worker function."""

    @patch("worker.process")
    def test_worker_processes_item(self, mock_process):
        mock_process.return_value = {"id": 1, "status": "ok", "message": "done"}
        q = queue.Queue()
        results = []
        q.put({"id": 1, "data": "test"})
        q.put(worker.SENTINEL)

        t = threading.Thread(target=worker.worker, args=(q, results))
        t.start()
        t.join(timeout=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "ok")

    @patch("worker.process", side_effect=RuntimeError("boom"))
    def test_worker_handles_failure(self, mock_process):
        q = queue.Queue()
        results = []
        q.put({"id": 1, "data": "test"})
        q.put(worker.SENTINEL)

        t = threading.Thread(target=worker.worker, args=(q, results))
        t.start()
        t.join(timeout=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "error")

    def test_worker_exits_on_sentinel(self):
        q = queue.Queue()
        results = []
        q.put(worker.SENTINEL)

        t = threading.Thread(target=worker.worker, args=(q, results))
        t.start()
        t.join(timeout=5)

        self.assertFalse(t.is_alive())
        self.assertEqual(len(results), 0)


class TestQueueLoop(unittest.TestCase):
    """Tests for queue_loop function."""

    def test_all_items_succeed(self):
        original_items = queue_loop.NUM_ITEMS
        original_workers = queue_loop.NUM_WORKERS
        queue_loop.NUM_ITEMS = 3
        queue_loop.NUM_WORKERS = 1
        try:
            summary = queue_loop.queue_loop()
        finally:
            queue_loop.NUM_ITEMS = original_items
            queue_loop.NUM_WORKERS = original_workers

        self.assertEqual(summary["completed"], 3)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(len(summary["results"]), 3)
        for r in summary["results"]:
            self.assertEqual(r["status"], "ok")

    def test_all_items_fail(self):
        original_items = queue_loop.NUM_ITEMS
        original_workers = queue_loop.NUM_WORKERS
        original_rate = work_item.FAILURE_RATE
        queue_loop.NUM_ITEMS = 3
        queue_loop.NUM_WORKERS = 1
        work_item.FAILURE_RATE = 1.0
        try:
            summary = queue_loop.queue_loop()
        finally:
            queue_loop.NUM_ITEMS = original_items
            queue_loop.NUM_WORKERS = original_workers
            work_item.FAILURE_RATE = original_rate

        self.assertEqual(summary["completed"], 0)
        self.assertEqual(summary["failed"], 3)
        for r in summary["results"]:
            self.assertEqual(r["status"], "error")


if __name__ == "__main__":
    unittest.main()
