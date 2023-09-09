#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId


class TestTaskId(unittest.TestCase):
    def test_task_id(self) -> None:
        ti = TaskId("test", 42)
        self.assertEqual(ti.node_id, "test")
        self.assertEqual(ti.id, 42)
        out = StreamOutput()
        ti.write_to(out)
        self.assertEqual(out.getvalue(), b"\x04test\x00\x00\x00\x00\x00\x00\x00\x2a")

        ti2 = TaskId()
        ti2.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(ti.node_id, "test")
        self.assertEqual(ti.id, 42)
        self.assertEqual(str(ti), "node=test, id=42")

    def test_empty_task_id(self) -> None:
        ti = TaskId()
        self.assertEqual(ti.node_id, "")
        self.assertIsNone(ti.id)
        out = StreamOutput()
        ti.write_to(out)
        self.assertEqual(out.getvalue(), b"\x00")
        self.assertEqual(str(ti), "node=, id=None")
