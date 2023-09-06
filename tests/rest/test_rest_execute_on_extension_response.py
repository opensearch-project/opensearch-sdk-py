#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestRestExecuteOnExtensionResponse(unittest.TestCase):
    def test_initialize_extension_request(self) -> None:
        reoer = RestExecuteOnExtensionResponse(status=RestStatus.OK, content_type="application/json; charset=utf-8", content=bytes("{}", "ascii"), headers={"foo": ["bar", "baz"]}, consumed_params=["bar", "baz"], content_consumed=True)
        self.assertEqual(reoer.status, RestStatus.OK)
        self.assertEqual(reoer.content_type, "application/json; charset=utf-8")
        self.assertEqual(reoer.content, bytes("{}", "ascii"))
        self.assertDictEqual(reoer.headers, {"foo": ["bar", "baz"]})
        self.assertListEqual(reoer.consumed_params, ["bar", "baz"])
        self.assertTrue(reoer.content_consumed)

        output = StreamOutput()
        reoer.write_to(output)

        reoer = RestExecuteOnExtensionResponse()
        reoer.read_from(StreamInput(output.getvalue()))
        self.assertEqual(reoer.status, RestStatus.OK)
        self.assertEqual(reoer.content_type, "application/json; charset=utf-8")
        self.assertEqual(reoer.content, bytes("{}", "ascii"))
        self.assertDictEqual(reoer.headers, {"foo": ["bar", "baz"]})
        self.assertListEqual(reoer.consumed_params, ["bar", "baz"])
        self.assertTrue(reoer.content_consumed)
