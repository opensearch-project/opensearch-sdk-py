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
from opensearch_sdk_py.rest.http_version import HttpVersion
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestExtensionRestRequest(unittest.TestCase):
    def test_initialize_extension_request(self) -> None:
        err = ExtensionRestRequest(
            method=RestMethod.GET,
            uri="/hello?v",
            path="/hello",
            params={"foo": "bar"},
            headers={"foo": ["bar", "baz"]},
            media_type="application/json; charset=utf-8",
            content=bytes("{}", "ascii"),
            principal_identifier_token="token",
            http_version=HttpVersion.HTTP_1_1,
        )
        self.assertEqual(err.method, RestMethod.GET)
        self.assertEqual(err.uri, "/hello?v")
        self.assertEqual(err.path, "/hello")
        self.assertDictEqual(err.params, {"foo": "bar"})
        self.assertDictEqual(err.headers, {"foo": ["bar", "baz"]})
        self.assertEqual(err.media_type, "application/json; charset=utf-8")
        self.assertEqual(err.content, bytes("{}", "ascii"))
        self.assertEqual(err.principal_identifier_token, "token")
        self.assertEqual(err.http_version, HttpVersion.HTTP_1_1)
        self.assertIn("method=RestMethod.GET, uri=/hello?v, path=/hello", str(err))

        output = StreamOutput()
        err.write_to(output)

        err = ExtensionRestRequest()
        err.read_from(StreamInput(output.getvalue()))
        self.assertEqual(err.method, RestMethod.GET)
        self.assertEqual(err.uri, "/hello?v")
        self.assertEqual(err.path, "/hello")
        self.assertDictEqual(err.params, {"foo": "bar"})
        self.assertDictEqual(err.headers, {"foo": ["bar", "baz"]})
        self.assertEqual(err.media_type, "application/json; charset=utf-8")
        self.assertEqual(err.content, bytes("{}", "ascii"))
        self.assertEqual(err.principal_identifier_token, "token")
        self.assertEqual(err.http_version, HttpVersion.HTTP_1_1)
