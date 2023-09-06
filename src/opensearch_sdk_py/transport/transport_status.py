#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
class TransportStatus:
    STATUS_REQRES = 1 << 0
    STATUS_ERROR = 1 << 1
    STATUS_COMPRESS = 1 << 2
    STATUS_HANDSHAKE = 1 << 3
