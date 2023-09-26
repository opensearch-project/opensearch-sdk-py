#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import json
import logging
import subprocess
import time
import unittest
from typing import Any, Generator

import httpx
import pytest


@pytest.fixture(scope="session")
def start_hello_extension() -> Generator:
    logging.debug("Starting hello extension ...")
    hello_cmd = ["poetry", "run", "samples/hello/hello.py"]
    hello_proc = subprocess.Popen(hello_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(1)
    logging.debug(f"Started process {hello_proc} ...")
    assert hello_proc.stdout
    assert not hello_proc.poll(), hello_proc.stdout.read().decode("utf-8")
    yield hello_proc
    logging.debug(f"Terminating PID {hello_proc.pid} ...")
    hello_proc.terminate()
    logging.info(f"STDOUT:\n\n{hello_proc.stdout.read().decode('utf-8')}")
    logging.debug(f"Terminated extension PID {hello_proc.pid} ...")


@pytest.fixture(scope="session")
def install_hello_extension() -> None:
    logging.debug("Installing hello extension ...")
    with open("samples/hello/hello.json") as f:
        ext = json.loads(f.read())
        logging.info(ext)
        response = httpx.post("http://localhost:9200/_extensions/initialize", json=ext)
        logging.debug(response.text)
        assert response.status_code == 202
        response_json = response.json()
        assert response_json["success"] == "A request to initialize an extension has been sent."
        time.sleep(3)
        logging.info("Installed hello extension ...")


@pytest.mark.usefixtures("start_hello_extension", "install_hello_extension")
class TestHello(unittest.TestCase):
    def test_hello_from_python(self) -> Any:
        response = httpx.get("http://localhost:9200/_extensions/_hello-world-py/hello")
        logging.debug(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello from Python! 👋\n")
