#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestExtensionRestResponse(unittest.TestCase):
    def test_initialize_extension_response(self) -> None:
        err = ExtensionRestResponse()
        self.assertEqual(err.content, b"")
        self.assertEqual(err.content_type, ExtensionRestResponse.TEXT_CONTENT_TYPE)
        self.assertDictEqual(err.headers, {})
        self.assertSetEqual(err.consumed_params, set())
        self.assertFalse(err.content_consumed)

        req = ExtensionRestRequest()
        req.param("foo")
        req.param("bar")
        req.content()
        err = ExtensionRestResponse(request=req, status=RestStatus.OK, content=b"test", content_type=ExtensionRestResponse.JSON_CONTENT_TYPE, headers={"foo": ["bar", "baz"]})
        self.assertEqual(err.status, RestStatus.OK)
        self.assertEqual(err.content, b"test")
        self.assertEqual(err.content_type, ExtensionRestResponse.JSON_CONTENT_TYPE)
        self.assertDictEqual(err.headers, {"foo": ["bar", "baz"]})
        self.assertSetEqual(err.consumed_params, {"foo", "bar"})
        self.assertTrue(err.content_consumed)

        output = StreamOutput()
        err.write_to(output)

        err = ExtensionRestResponse()
        err.read_from(StreamInput(output.getvalue()))
        self.assertEqual(err.status, RestStatus.OK)
        self.assertEqual(err.content, b"test")
        self.assertEqual(err.content_type, ExtensionRestResponse.JSON_CONTENT_TYPE)
        self.assertDictEqual(err.headers, {"foo": ["bar", "baz"]})
        self.assertSetEqual(err.consumed_params, {"foo", "bar"})
        self.assertTrue(err.content_consumed)
