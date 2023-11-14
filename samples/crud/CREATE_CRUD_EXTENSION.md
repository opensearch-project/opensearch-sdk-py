# Creating a Basic CRUD Extension

This guide provides step-by-step instructions on creating a basic CRUD (Create, Read, Update, Delete) extension for OpenSearch using Python. This extension allows you to perform operations on an index, including creating, reading, updating, and deleting documents.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Implement the Extension Interface](#implement-the-extension-interface)
- [Implement the REST Handler](#implement-the-rest-handler)
- [Writing CRUD methods](#writing-crud-methods)
- [Register the Extension](#register-the-extension)

## Prerequisites
- OpenSearch installed and running.
- Python installed on your system.

## Initial Setup

**Install Required Packages:** Install necessary Python packages using `pip`:

```bash
pip install opensearchpy
```

## Implement the Extension Interface

Create a class that implements the Extension interface. You can extend the Extension class 
to inherit default implementations of extension interface and ActionExtension class for rest handling.

```python
from crud_handler import CRUDRestHandler

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler


class CRUDExtension(Extension, ActionExtension):
    def __init__(self) -> None:
        Extension.__init__(self, "crud-py")
        ActionExtension.__init__(self)
    
    @property
    def rest_handlers(self) -> list[ExtensionRestHandler]:
        return [CRUDRestHandler()]
```

## Implement the REST Handler

Create a class that implements the ExtensionRestHandler interface. You can extend the ExtensionRestHandler class.

```python
from opensearchpy import OpenSearch
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest

import logging
import json

logging.basicConfig(encoding="utf-8", level=logging.INFO)

class CRUDRestHandler(ExtensionRestHandler):
    def __init__(self) -> None:
        self.client = OpenSearch(
            hosts=[{'host': 'localhost', 'port': 9200}],
            http_auth=('admin', 'admin'),  # For testing only. Don't store credentials in code.
            use_ssl=False,
            verify_certs=False,
            ssl_show_warn=False
        )

    def handle_request(self, request: ExtensionRestRequest) -> ExtensionRestResponse:
        logging.info(f"handling {request}")
        logging.info(f"request method: {request.method}")

        if request.method == RestMethod.POST:
            # Create a document
            index_name = 'test-index'
            document = request.content
            response = self.client.index(
                index=index_name,
                body=document,
                refresh=True
            ) 
            response_bytes = bytes(json.dumps(response).encode("utf-8"))
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)
        
        elif request.method == RestMethod.GET:
            # Search for documents
            index_name = "test-index"
            q = request.param("q")

            logging.info(f"inside get {q}")

            query = {
                'size': 5,
                'query': {
                    'multi_match': {
                        'query': q,
                        'fields': ['title^2', 'director']
                    }
                }
            }
            response = self.client.search(
                body=query,
                index=index_name
            )
            response_bytes = bytes(json.dumps(response).encode("utf-8"))
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        elif request.method == RestMethod.PUT:
            # Update a document
            index_name = "test-index"            
            id = request.param("id")
            document = request.content
            response = self.client.index(index=index_name, body=document, id=id, refresh=True)
            response_bytes = bytes(json.dumps(response), "utf-8")
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        elif request.method == RestMethod.DELETE:
            # Delete a document
            index_name = "test-index"
            id = request.param("id")
            response = self.client.delete(
                index=index_name,
                id=id
            )
            response_bytes = bytes(json.dumps(response), "utf-8")
            logging.info(f"response: {response}")
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        else:
            return ExtensionRestResponse(RestStatus.NOT_FOUND, bytes("Not found", "utf-8"), ExtensionRestResponse.TEXT_CONTENT_TYPE)
        
    @property
    def routes(self) -> list[NamedRoute]:
        return [NamedRoute(method=RestMethod.POST, path="/crud", unique_name="crud_post"),
                NamedRoute(method=RestMethod.GET, path="/crud", unique_name="crud_get"),
                NamedRoute(method=RestMethod.PUT, path="/crud", unique_name="crud_put"),
                NamedRoute(method=RestMethod.DELETE, path="/crud", unique_name="crud_delete")]
```
ExtensionRestHandler provides a handle_request method that takes an ExtensionRestRequest and returns an ExtensionRestResponse. The ExtensionRestRequest contains the request method, content, and parameters. The ExtensionRestResponse contains the response status, content, and content type.

Also implement the routes property to define the routes that the extension will handle. The routes property returns a list of NamedRoute objects. Each NamedRoute object contains the request method, path, and unique name.

## Writing CRUD methods

The CRUD extension will handle the following methods:

- POST /crud: Create a document
    ```
    index_name = 'test-index'
                document = request.content
                response = self.client.index(
                    index=index_name,
                    body=document,
                    refresh=True
                ) 
                response_bytes = bytes(json.dumps(response).encode("utf-8"))
                return ExtensionRestResponse(RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)
    ```
    post method takes a document as input and creates a document in the index. The document is passed as the request content. The response is returned as a JSON object.

- GET /crud: Search for documents
    ```
    index_name = 'test-index'
    q = request.param("q")
    
    logging.info(f"inside get {q}")

    query = {
        'size': 5,
        'query': {
            'multi_match': {
                'query': q,
                'fields': ['title^2', 'director']
            }
        }
    }
    response = self.client.search(
        body=query,
        index=index_name
    )
    response_bytes = bytes(json.dumps(response).encode("utf-8"))
    return ExtensionRestResponse(RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE, consumed_params=["q"])
    ```
    get method takes a query parameter `q` and searches for documents in the index with the given query. We have mentioned `consumed_params=["q"]` to indicate that the extension has consumed the `q` parameter.

- PUT /crud: Update a document
    ```
    index_name = 'test-index'
    id = request.param("id")
    document = request.content
    response = self.client.index(
        index=index_name,
        body=document,
        id=id,
        refresh=True
    )
    response_bytes = bytes(json.dumps(response), "utf-8")
    return ExtensionRestResponse(RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE, consumed_params=["id"])
    ```
    put method takes an id parameter and updates the document with the given id in the index. The document is passed as the request content. We have mentioned `consumed_params=["id"]` to indicate that the extension has consumed the `id` parameter.

- DELETE /crud: Delete a document
    ```
    index_name = 'test-index'
    id = request.param("id")
    response = self.client.delete(
        index=index_name,
        id=id
    )
    response_bytes = bytes(json.dumps(response), "utf-8")
    logging.info(f"response: {response}")
    return ExtensionRestResponse(RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE, consumed_params=["id"])
    ```
    delete method takes an id parameter and deletes the document with the given id from the index. We have mentioned `consumed_params=["id"]` to indicate that the extension has consumed the `id` parameter.

## Register the Extension

Register the extension with OpenSearch by sending a POST request to the _extension/initialize endpoint. The request body should contain the extension name and the path to the extension.json file.

```bash
curl -XPOST "localhost:9200/_extensions/initialize" -H "Content-Type:application/json" --data @samples/crud/crud.json

{"success":"A request to initialize an extension has been sent."}
```