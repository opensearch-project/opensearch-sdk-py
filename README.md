- [OpenSearch Python SDK](#opensearch-python-sdk)
    - [Developing](#developing)
    - [Copyright and License](#copyright-and-license)

# OpenSearch Python SDK

[![tests](https://github.com/opensearch-project/opensearch-sdk-py/actions/workflows/test.yml/badge.svg)](https://github.com/opensearch-project/opensearch-sdk-py/actions/workflows/test.yml)

The experimental OpenSearch Python SDK enables you to implement Extensions that provide additional functionality to OpenSearch by registering that functionality through a set of extension points.

When OpenSearch functionality is provided by a REST API, Extensions will use the OpenSearch Python Client to implement it. However, when REST APIs do not provide this information, its binary transport protocol is used. That protocol is implemented in this SDK. Unlike the [OpenSearch Java SDK](https://github.com/opensearch-project/opensearch-sdk-java) the Python implementation reimplements the protocol in pure python.

See [samples/hello](samples/hello/README.md) to get started.

### Developing

See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for implementation details.

### Copyright and License

See [LICENSE](LICENSE.txt)