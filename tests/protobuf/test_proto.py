#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.protobuf import ExtensionIdentityProto_pb2, RegisterRestActionsProto_pb2
from google._upb._message import FileDescriptor


class TestProto(unittest.TestCase):

    # The DESCRIPTOR constant in the generated files is not covered
    def test_file_descriptors(self) -> None:
        self.assertIsInstance(ExtensionIdentityProto_pb2.DESCRIPTOR, FileDescriptor)
        self.assertIsInstance(RegisterRestActionsProto_pb2.DESCRIPTOR, FileDescriptor)
