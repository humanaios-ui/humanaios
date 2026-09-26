#!/usr/bin/env python3
"""
T1-D: Integration Tests for Batch Sync Infrastructure

Tests:
1. Batch accumulation (max 10, 30s window)
2. Atomic dispatch with Admiral signatures
3. Fallback queueing on failure
4. Crash recovery
5. Idempotency verification
"""

import unittest
import time
import tempfile
import sqlite3
from pathlib import Path
from batch_sync_infrastructure import (
    BatchAccumulator, AtomicDispatcher, PersistentQueue,
    BatchSyncCoordinator, Message, MessagePriority
)


class TestBatchAccumulator(unittest.TestCase):
    """Test T1-A: Batch accumulation logic"""

    def setUp(self):
        self.accumulator = BatchAccumulator()

    def test_accumulate_single_message(self):
        """Test accumulating single message"""
        msg = Message(
            message_id="msg_1",
            source_claude="empirica-foundation-evaluator",
            target_claudes=["empirica-autonomy"],
            payload={"decision": "test"},
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            idempotency_key="prop_1"
        )

        ready, batch = self.accumulator.add_message(msg)
        self.assertFalse(ready, "Single message shouldn't trigger dispatch")
        self.assertEqual(len(self.accumulator.messages), 1)

    def test_accumulate_to_max_size(self):
        """Test batch dispatch at max size (10 messages)"""
        for i in range(BatchAccumulator.MAX_BATCH_SIZE):
            msg = Message(
                message_id=f"msg_{i}",
                source_claude="empirica-foundation-evaluator",
                target_claudes=[f"practice_{i}"],
                payload={"index": i},
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                idempotency_key=f"prop_{i}"
            )
            ready, batch = self.accumulator.add_message(msg)

        # Last message should trigger dispatch
        self.assertTrue(ready, "Max batch size should trigger dispatch")
        self.assertEqual(len(batch), BatchAccumulator.MAX_BATCH_SIZE)

    def test_priority_ordering(self):
        """Test messages are sorted by priority"""
        # Add messages in reverse priority order
        messages = [
            (MessagePriority.LOW, "msg_low"),
            (MessagePriority.NORMAL, "msg_normal"),
            (MessagePriority.HIGH, "msg_high"),
            (MessagePriority.CRITICAL, "msg_critical"),
        ]

        for priority, msg_id in messages:
            msg = Message(
                message_id=msg_id,
                source_claude="empirica-foundation-evaluator",
                target_claudes=["empirica-autonomy"],
                payload={},
                priority=priority,
                timestamp=time.time(),
                idempotency_key=msg_id
            )
            self.accumulator.add_message(msg)

        # Force flush
        batch = self.accumulator.flush()

        # Verify ordering: CRITICAL(0) < HIGH(1) < NORMAL(2) < LOW(3)
        priorities = [msg.priority.value for msg in batch]
        self.assertEqual(priorities, [0, 1, 2, 3], "Messages not ordered by priority")

    def test_window_timeout(self):
        """Test batch dispatch after window timeout"""
        msg = Message(
            message_id="msg_1",
            source_claude="empirica-foundation-evaluator",
            target_claudes=["empirica-autonomy"],
            payload={},
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            idempotency_key="prop_1"
        )

        # Add message
        self.accumulator.add_message(msg)

        # Simulate window expiry by advancing window_start
        self.accumulator.window_start = time.time() - (BatchAccumulator.WINDOW_SECONDS + 1)

        # Add another message - should trigger dispatch
        msg2 = Message(
            message_id="msg_2",
            source_claude="empirica-foundation-evaluator",
            target_claudes=["empirica-autonomy"],
            payload={},
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            idempotency_key="prop_2"
        )
        ready, batch = self.accumulator.add_message(msg2)

        self.assertTrue(ready, "Window timeout should trigger dispatch")


class TestAtomicDispatcher(unittest.TestCase):
    """Test T1-B: Atomic dispatch"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.dispatcher = AtomicDispatcher(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_dispatch_with_signature(self):
        """Test dispatching batch with Admiral signature"""
        messages = [
            Message(
                message_id="msg_1",
                source_claude="admiral",
                target_claudes=["empirica-autonomy"],
                payload={"decision": "test"},
                priority=MessagePriority.CRITICAL,
                timestamp=time.time(),
                idempotency_key="prop_1"
            )
        ]

        success, msg = self.dispatcher.dispatch_batch(
            messages,
            admiral_signature="mock_signature_12345",
            transaction_id="txn_test"
        )

        self.assertTrue(success, "Dispatch should succeed with valid signature")

    def test_idempotency_check(self):
        """Test idempotency key checking"""
        # Create duplicate idempotency keys
        messages = [
            Message(
                message_id="msg_1",
                source_claude="admiral",
                target_claudes=["empirica-autonomy"],
                payload={},
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                idempotency_key="duplicate_key"
            ),
            Message(
                message_id="msg_2",
                source_claude="admiral",
                target_claudes=["empirica-autonomy"],
                payload={},
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                idempotency_key="duplicate_key"  # Same key
            )
        ]

        success, msg = self.dispatcher.dispatch_batch(
            messages,
            admiral_signature="mock_sig",
            transaction_id="txn_test"
        )

        self.assertFalse(success, "Should reject duplicate idempotency keys")


class TestPersistentQueue(unittest.TestCase):
    """Test T1-C: Fallback queue"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.queue = PersistentQueue(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_queue_initialization(self):
        """Test queue tables created on init"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        self.assertIn("empirica_dispatch_log", tables)
        self.assertIn("empirica_retry_queue", tables)
        self.assertIn("empirica_dead_letter_queue", tables)

        conn.close()

    def test_pending_retries_retrieval(self):
        """Test getting pending retries"""
        pending = self.queue.get_pending_retries()
        # Should return empty list initially
        self.assertEqual(pending, [])


class TestBatchSyncCoordinator(unittest.TestCase):
    """Test T1-D: Full integration"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.coordinator = BatchSyncCoordinator(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_end_to_end_message_processing(self):
        """Test full message flow"""
        # Process messages until batch is ready
        for i in range(BatchAccumulator.MAX_BATCH_SIZE):
            msg = Message(
                message_id=f"msg_{i}",
                source_claude="empirica-foundation-evaluator",
                target_claudes=["empirica-autonomy"],
                payload={"index": i},
                priority=MessagePriority.NORMAL if i % 2 == 0 else MessagePriority.HIGH,
                timestamp=time.time(),
                idempotency_key=f"prop_{i}"
            )

            if i < BatchAccumulator.MAX_BATCH_SIZE - 1:
                success, status = self.coordinator.process_message(msg, "mock_sig")
                self.assertTrue(success)
                self.assertIn("Queued", status)
            else:
                # Last message triggers dispatch
                success, status = self.coordinator.process_message(msg, "mock_sig")
                self.assertTrue(success)

    def test_crash_recovery(self):
        """Test recovering from crash"""
        # Add message to queue
        msg = Message(
            message_id="msg_crash_test",
            source_claude="empirica-foundation-evaluator",
            target_claudes=["empirica-autonomy"],
            payload={},
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            idempotency_key="prop_crash"
        )

        self.coordinator.process_message(msg, "mock_sig")

        # Simulate crash recovery
        recovered = self.coordinator.recover_from_crash()

        # Should recover without errors
        self.assertIsInstance(recovered, int)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
