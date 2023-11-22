#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from enum import Enum


class RequestType(Enum):
    REQUEST_EXTENSION_CLUSTER_STATE = 0
    REQUEST_EXTENSION_CLUSTER_SETTINGS = 1
    REQUEST_EXTENSION_REGISTER_REST_ACTIONS = 2
    REQUEST_EXTENSION_REGISTER_SETTINGS = 3
    REQUEST_EXTENSION_ENVIRONMENT_SETTINGS = 4
    REQUEST_EXTENSION_DEPENDENCY_INFORMATION = 5
    CREATE_COMPONENT = 6
    ON_INDEX_MODULE = 7
    GET_SETTINGS = 8
