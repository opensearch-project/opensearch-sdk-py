#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from hello_extension import HelloExtension

from opensearch_sdk_py.server.async_extension_host import AsyncExtensionHost

logging.basicConfig(encoding="utf-8", level=logging.INFO)

extension = HelloExtension()
logging.info(f"Starting {extension} that implements {extension.implemented_interfaces}.")

host = AsyncExtensionHost()
host.serve(extension)

logging.info(f"Listening on {host.address}:{host.port}.")
host.run()
