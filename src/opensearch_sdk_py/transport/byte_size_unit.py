#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from enum import Enum

ByteSizeUnit = Enum("ByteSizeUnit", ["BYTES", "KB", "MB", "GB", "TB", "PB"], start=0)
