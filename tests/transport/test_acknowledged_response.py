#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestAcknowledgedResponse(unittest.TestCase):
    def test_initialize_extension_response(self) -> None:
        ar = AcknowledgedResponse()
        self.assertFalse(ar.status)
        self.assertEqual(str(ar), "status=False")

        ar = AcknowledgedResponse(True)
        self.assertTrue(ar.status)
        self.assertEqual(str(ar), "status=True")

        out = StreamOutput()
        ar.write_to(out)

        input = StreamInput(out.getvalue())
        ar = AcknowledgedResponse().read_from(input)
        self.assertTrue(ar.status)
