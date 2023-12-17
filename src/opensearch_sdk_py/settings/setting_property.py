#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from enum import Enum

SettingProperty = Enum("SettingProperty", ["FILTERED", "DYNAMIC", "FINAL", "DEPRECATED", "NODE_SCOPE", "CONSISTENT", "INDEX_SCOPE", "NOT_COPYABLE_ON_RESIZE", "INTERNAL_INDEX", "PRIVATE_INDEX", "EXTENSION_SCOPE"], start=0)
