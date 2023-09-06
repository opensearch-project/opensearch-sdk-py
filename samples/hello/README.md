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
INFO:root:< server=<socket.socket fd=7, family=2, type=1, proto=0, laddr=('127.0.0.1', 1234)>
INFO:root:< prefix=b'ES', version=2.10.0.99, type=['request', 'handshake'], message=49 byte(s), id=8, ctx=req={}, res={}, None
INFO:root:> prefix=b'ES', version=2.10.0.99, type=['response', 'handshake'], message=23 byte(s), id=8, ctx=req={}, res={}, version=2.10.0.99, features=[], size=29 byte(s)
INFO:root:< prefix=b'ES', version=2.10.0.99, type=['request'], message=50 byte(s), id=9, ctx=req={}, res={}, None
INFO:root:> prefix=b'ES', version=2.10.0.99, type=['response'], message=179 byte(s), id=9, ctx=req={}, res={}, id=hello-world, version=3.0.0.99, name=hello-world, host=127.0.0.1, addr=127.0.0.1, attr={}, roles={('ingest', 'i', False), ('remote_cluster_client', 'r', False), ('data', 'd', True), ('cluster_manager', 'm', False)}, cluster name=, version=3.0.0.99, features=[], size=185 byte(s)
INFO:root:< prefix=b'ES', version=2.10.0.99, type=['request'], message=469 byte(s), id=10, ctx=req={'_system_index_access_allowed': 'false'}, res={}, None
INFO:root:> prefix=b'ES', version=2.10.0.99, type=['request'], message=167 byte(s), id=101, ctx=req={'_system_index_access_allowed': 'false', 'extension_unique_id': 'hello-world'}, res={}, node=, id=-1, size=173 byte(s)
INFO:root:> prefix=b'ES', version=2.10.0.99, type=['response'], message=125 byte(s), id=10, ctx=req={'extension_unique_id': 'hello-world', '_system_index_access_allowed': 'false'}, res={}, name=hello-world, interfaces=['Extension', 'ActionExtension'], features=[]
```