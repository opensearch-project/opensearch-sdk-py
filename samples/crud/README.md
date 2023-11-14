# OpenSearch CRUD Extension

This extension allows you to perform CRUD (Create, Read, Update, Delete) operations in OpenSearch. It exposes a REST API for managing data.

## Table of Contents

- [CRUD Extension](#crud-extension)
  - [Start OpenSearch](#start-opensearch)
  - [Start the Extension](#start-the-extension)
  - [Register the Extension](#register-the-extension)
  - [Call an Extension API](#call-an-extension-api)

## CRUD Extension

This sample implements an extension that exposes a REST API's for CRUD operations.

### Start OpenSearch

Start OpenSearch as described in the [the developer guide](https://github.com/opensearch-project/opensearch-sdk-java/blob/main/DEVELOPER_GUIDE.md#start-opensearch).

### Start the Extension

```bash
poetry install
poetry run samples/crud_extension/crud.py
```
This will start an extension that will be listening on TCP port 1234, talking the OpenSearch protocol.

### Register the Extension

``` bash
curl -XPOST "localhost:9200/_extensions/initialize" -H "Content-Type:application/json" --data @samples/crud_extension/crud.json

{"success":"A request to initialize an extension has been sent."}
```

You should see some output on the extension.

``` bash
INFO:root:< prefix=b'ES', version=2.12.0.99, type=['request'], message=468 byte(s), id=32, ctx=req={'_system_index_access_allowed': 'false'}, res={}, None, features=[], action=internal:discovery/extensions
INFO:root:> prefix=b'ES', version=2.12.0.99, type=['request'], message=195 byte(s), id=6, ctx=req={'_system_index_access_allowed': 'false'}, res={}, node=, id=None, features=[], action=internal:discovery/registerrestactions, size=201 byte(s)
INFO:root:b'ES\x00\x00\x007\x00\x00\x00\x00\x00\x00\x00\x06\x01\x08 Y\xa3\x00\x00\x00%\x01\x1c_system_index_access_allowed\x05false\x00\x01'
INFO:root:< response prefix=b'ES', version=2.12.0.99, type=['response'], message=55 byte(s), id=6, ctx=req={'_system_index_access_allowed': 'false'}, res={}, None, features=[]
INFO:root:> prefix=b'ES', version=2.12.0.99, type=['response'], message=89 byte(s), id=32, ctx=req={'_system_index_access_allowed': 'false'}, res={}, name=crud-py, interfaces=['Extension', 'ActionExtension'], features=[], size=95 byte(s)
```

### Call an Extension API

#### Create a document

```bash
curl -XPOST "localhost:9200/_extensions/_crud-py/crud" -H "Content-Type:application/json" --data '{
  "title": "Moneyball",
  "director": "Bennett Miller",
  "year": "2011"
}'

{"_index": "test-index", "_id": "gDTedIsBNJHV14IHbeqe", "_version": 1, "result": "created", "forced_refresh": true, "_shards": {"total": 2, "successful": 1, "failed": 0}, "_seq_no": 0, "_primary_term": 1}
```

#### Read a document

```bash
curl -XGET "localhost:9200/_extensions/_crud-py/crud?q=Miller"

{"took": 145, "timed_out": false, "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0}, "hits": {"total": {"value": 1, "relation": "eq"}, "max_score": 0.2876821, "hits": [{"_index": "test-index", "_id": "gDTedIsBNJHV14IHbeqe", "_score": 0.2876821, "_source": {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}}]}}
```

#### Update a document

```bash
curl -XPUT "localhost:9200/_extensions/_crud-py/crud?id=gDTedIsBNJHV14IHbeqe" -H "Content-Type:application/json" --data '{
  "title": "Moneyball",
  "director": "Bennett Miller",
  "year": "2011",
  "rating": "PG-13"
}'

{"_index": "test-index", "_id": "gDTedIsBNJHV14IHbeqe", "_version": 2, "result": "updated", "forced_refresh": true, "_shards": {"total": 2, "successful": 1, "failed": 0}, "_seq_no": 1, "_primary_term": 1}
```

#### Delete a document

```bash
curl -XDELETE "localhost:9200/_extensions/_crud-py/crud?id=gDTedIsBNJHV14IHbeqe"

{"_index": "test-index", "_id": "1f3zdIsBEBq5u0bwfSOP", "_version": 2, "result": "deleted", "_shards": {"total": 2, "successful": 1, "failed": 0}, "_seq_no": 1, "_primary_term": 1}
```