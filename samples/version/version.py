#!/usr/bin/env python

import logging
from opensearch_sdk_py.transport.version import Version

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logging.info(Version(2100099))
