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
from opensearch_sdk_py.transport.transport_request import TransportRequest


class TestTransportRequest(unittest.TestCase):
    def test_transport_request(self) -> None:
        tr = TransportRequest(TaskId("test", 42))
        self.assertEqual(tr.parent_task_id.node_id, "test")
        self.assertEqual(tr.parent_task_id.id, 42)

        out = StreamOutput()
        tr.write_to(out)
        out.write(b"\x01\x02\x03")
        self.assertEqual(out.getvalue(), b"\x04test\x00\x00\x00\x00\x00\x00\x00\x2a\x01\x02\x03")

        tr = TransportRequest()
        self.assertEqual(tr.parent_task_id.node_id, "")
        self.assertIsNone(tr.parent_task_id.id)
        tr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(tr.parent_task_id.node_id, "test")
        self.assertEqual(tr.parent_task_id.id, 42)
        self.assertEqual(str(tr), "node=test, id=42")
