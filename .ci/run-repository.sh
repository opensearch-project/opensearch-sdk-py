#!/usr/bin/env bash

#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Launch one or more OpenSearch nodes via the Docker image,
# to form a cluster suitable for running the REST API tests.
#

# Called by entry point `run-test` use this script to add your repository specific test commands
# Once called opensearch is up and running and the following parameters are available to this script.

# OPENSEARCH_VERSION -- version e.g Major.Minor.Patch(-Prelease)
# OPENSEARCH_URL -- the url at which opensearch is reachable
# network_name -- the docker network name
# NODE_NAME -- the docker container name also used as opensearch node name

set -e

echo -e "\033[34;1mINFO:\033[0m URL ${opensearch_url}\033[0m"
echo -e "\033[34;1mINFO:\033[0m VERSION ${OPENSEARCH_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION ${PYTHON_VERSION}\033[0m"

echo -e "\033[1m>>>>> Build [opensearch-project/opensearch-sdk-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

docker build \
       --file .ci/Dockerfile.client \
       --tag opensearch-project/opensearch-sdk-py \
       --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
       .

echo -e "\033[1m>>>>> Run [opensearch-project/opensearch-sdk-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

docker run \
  --network=${network_name} \
  --env "OPENSEARCH_URL=${opensearch_url}" \
  --env "OPENSEARCH_VERSION=${OPENSEARCH_VERSION}" \
  --env "TEST_PATTERN=${TEST_PATTERN}" \
  --name opensearch-sdk-py \
  --rm \
  opensearch-project/opensearch-sdk-py \
  poetry run pytest ${TEST_PATTERN}
