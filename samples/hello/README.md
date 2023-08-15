# Hello World

### Start OpenSearch

Enable the `opensearch.experimental.feature.extensions.enabled` experimental feature in either way described in [the developer guide](https://github.com/opensearch-project/opensearch-sdk-java/blob/main/DEVELOPER_GUIDE.md#enable-the-extensions-feature-flag).

For example, edit `gradle/run.gradle` in OpenSearch source from `main`.

```
testClusters {
  runTask {
    ...
    systemProperty 'opensearch.experimental.feature.extensions.enabled', 'true'
  }
}
```

Run OpenSearch.

```bash
./gradlew run
```

You should see a line in the logs.

```
[2023-08-15T12:22:30,661][INFO ][o.o.e.ExtensionsManager  ] [runTask-0] ExtensionsManager initialized
```

This will start a local instance of OpenSearch with the experimental extensions feature enabled.

Check that the server is running.

```bash
curl http://localhost:9200

{
  "name" : "runTask-0",
  "cluster_name" : "runTask",
  "cluster_uuid" : "VdCBimtZRzyWc0ApWIf0EQ",
  "version" : {
    "distribution" : "opensearch",
    "number" : "3.0.0-SNAPSHOT",
    "build_type" : "tar",
    "build_hash" : "34c860d82be75136ce3cef60fcd9523f1e86afd5",
    "build_date" : "2023-08-15T16:08:29.011959Z",
    "build_snapshot" : true,
    "lucene_version" : "9.8.0",
    "minimum_wire_compatibility_version" : "2.10.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

### Start the Extension

```bash
poetry install
poetry run samples/hello/hello.py
```

This will start an extension that will be listening on TCP port 1234, talking the OpenSearch protocol.

### Register the Extension

```bash
curl -XPOST "localhost:9200/_extensions/initialize" -H "Content-Type:application/json" --data @samples/hello/hello.json

{"success":"A request to initialize an extension has been sent."}
```

You should see some output on the extension.

```
received <opensearch_sdk_py.transport.stream_input.StreamInput object at 0x104e02450>, 55 byte(s)
	#b'ES\x00\x00\x001\x00\x00\x00\x00\x00\x00\x00\n\x08\x08 \x0b\x83\x00\x00\x00\x1a\x00\x00\x00\x16internal:tcp/handshake\x00\x04\xa3\x8e\xb7A'
	handshake b'ES', message=49 byte(s), request_id=10, status=8, version=2.10.0.99

received <opensearch_sdk_py.transport.stream_input.StreamInput object at 0x10442a050>, 29 byte(s)
	#b'ES\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\n\t\x08 \x0b\x83\x00\x00\x00\x02\x00\x00\xa3\x8e\xb7A'
	handshake b'ES', message=23 byte(s), request_id=10, status=9, version=2.10.0.99

received <opensearch_sdk_py.transport.stream_input.StreamInput object at 0x104e01d90>, 56 byte(s)
	#b'ES\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x08-\xc7#\x00\x00\x00 \x00\x00\x00\x1cinternal:transport/handshake\x00'
	request b'ES', message=50 byte(s), request_id=11, status=0, version=3.0.0.99
```