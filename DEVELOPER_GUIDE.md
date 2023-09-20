- [Forking and Cloning](#forking-and-cloning)
- [Building and Testing](#building-and-testing)
  - [Install Pyenv](#install-pyenv)
  - [Install Python 3.9](#install-python-39)
  - [Install Poetry](#install-poetry)
  - [Install Dependencies](#install-dependencies)
  - [Run Tests](#run-tests)
  - [Run OpenSearch](#run-opensearch)
  - [Run Integration Tests](#run-integration-tests)
  - [Install Pre Commit](#install-pre-commit)
- [Developing](#developing)
  - [Code Linting](#code-linting)
  - [Type Checking](#type-checking)
  - [Code Coverage](#code-coverage)
- [License Headers](#license-headers)
  - [Visual Studio Code](#visual-studio-code)
- [Transport Protocol](#transport-protocol)
  - [Overview](#overview)
  - [REST Handlers](#rest-handlers)
  - [Transport Actions](#transport-actions)
  - [Transport Protocol](#transport-protocol-1)

## Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.

## Building and Testing

### Install Pyenv

Use pyenv to manage multiple versions of Python. This can be installed with [pyenv-installer](https://github.com/pyenv/pyenv-installer) on Linux and MacOS, and [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) on Windows.

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

### Install Python 3.9

Python projects in this repository use Python 3.9. See the [Python Beginners Guide](https://wiki.python.org/moin/BeginnersGuide) if you have never worked with the language.

```
$ python --version
Python 3.9.16
```

If you are using pyenv.

```
pyenv install 3.9
pyenv global 3.9
```

### Install Poetry

This project uses [poetry](https://python-poetry.org/), which is typically installed with `curl -sSL https://install.python-poetry.org | python3 -`. Poetry automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your `pyproject.toml` as you install/uninstall packages. It also generates the ever-important `poetry.lock`, which is used to produce deterministic builds.

```
$ pip install poetry

$ poetry --version
Poetry (version 1.5.1)
```

### Install Dependencies

```
poetry install
```

### Run Tests

Run tests and ensure they pass.

```
poetry run pytest -v
```

### Run OpenSearch

Set the value of `opensearch.experimental.feature.extensions.enabled` to `true` as described in [the developer guide](https://github.com/opensearch-project/opensearch-sdk-java/blob/main/DEVELOPER_GUIDE.md#enable-the-extensions-feature-flag).

For example, check out [OpenSearch](https://github.com/opensearch-project/OpenSearch) with `git clone`, then edit `gradle/run.gradle`.

```
testClusters {
  runTask {
    ...
    systemProperty 'opensearch.experimental.feature.extensions.enabled', 'true'
  }
}
```

When you start OpenSearch with `./gradlew run` you will see the following line in the logs.

```
[2023-08-15T12:22:30,661][INFO ][o.o.e.ExtensionsManager  ] [runTask-0] ExtensionsManager initialized
```

### Run Integration Tests

Run integration tests and a locally running instance of OpenSearch as described above.

```
poetry exec integration
```

This will start and install the [hello sample](samples/hello) and execute some tests.

### Install Pre Commit

This project uses a [pre-commit hook](https://pre-commit.com/) for linting Python code which is then checked in the [lint workflow](.github/workflows/lint.ml).
.

```
$ poetry run pre-commit install
$ poetry run pre-commit run --all-files
```

Pre-commit hook will run `isort`, `flake8`, `mypy` and `pytest` before making a commit.

## Developing

### Code Linting

This project uses a set of tools, such as [isort](https://github.com/PyCQA/isort) to ensure that imports are sorted, and [flake8](https://flake8.pycqa.org/en/latest/) to enforce code style.

```
$ poetry run flake8
./src/assemble_workflow/bundle_recorder.py:30:13: W503 line break before binary operator
```

Use `isort .` to fix any sorting order.

```
$ poetry run isort .
Fixing tests/system/test_arch.py
```

Use [black](https://black.readthedocs.io/en/stable/) to auto-format your code.

```
$ poetry run black .
All done! ✨ 🍰 ✨
23 files left unchanged.
```

You can run a combination of these tools by installing [poetry-exec-plugin](https://github.com/keattang/poetry-exec-plugin) once.

```
poetry self add poetry-exec-plugin
```

Then use `poetry exec auto`.

### Type Checking

This project uses [mypy](https://github.com/python/mypy) as an optional static type checker. Make sure that `poetry run mypy .` is clean before making pull requests.

### Code Coverage

This project uses [codecov](https://about.codecov.io/) for code coverage. Use `poetry run coverage` to run code coverage locally.

```
$ poetry run coverage run --source=src -m pytest
47 passed in 5.89s

$ poetry run coverage report
TOTAL 1207 79 93%
```

You can run a combination of these by installing [poetry-exec-plugin](https://github.com/keattang/poetry-exec-plugin) once and using the `poetry exec coverage` shortcut.

## License Headers

All python code has a copy of the [license header](LICENSE_HEADER.txt) on top of it. To bulk apply license headers use `poetry run licenseheaders -t LICENSE_HEADER.txt -E .py`.

### Visual Studio Code

After opening Visual Studio Code, use `> Pythin: Select Interpreter` (also in the bottom right of VSCode when you edit a Python file) to properly resolve import paths.

## Transport Protocol

### Overview

The primary purpose of the SDK is to permit Extensions to provide additional functionality to OpenSearch by registering that functionality through a set of extension points. Development on this project is focused on providing these extension points. When OpenSearch functionality is provided by a REST API, Extensions will use the OpenSearch Python Client to implement it. However, when REST APIs do not provide this information, its binary transport protocol is used. That protocol is implemented in this SDK.

### REST Handlers

One example of an extension point is REST handler registration. An extension communicates to OpenSearch which REST requests it will handle, and OpenSearch redirects those requests to the extension. This requires the SDK to implement two request-response workflows, one to register the supported REST methods and paths, and one to implement the functionality and return an appropriate response.

### Transport Actions

A transport action's request-response workflow has 4 key components.

1. A request class containing information needed to execute.
2. A response class, which may simply acknowledge the request or provide requested information.
3. A handler class on whichever side of the connection is handling the request and returning the response.
4. A name, used to uniquely identify the above three components.

In the REST handler registration example, the SDK sends the request, which includes the API name. OpenSearch implements a handler that adds the new paths to the RestController and returns an acknowledge response to the SDK.

When the user makes a REST request, OpenSearch forwards the request to the SDK which must handle it. This handler will be provided by SDK implementers in the form of a class and function to take the request as input and return an appropriate response as output, which is then returned by the SDK to OpenSearch and ultimately to the user.

The Request and Response classes extend the `TransportMessage` class and implement `read_from()` and `write_to()` methods to communicate information via byte streams. When porting functionality from OpenSearch classes, care must be taken to precisely match the type of writeable stream values, which correspond to common cross-language primitives. These `TransportMessage` instances are passed as parameters to an `OutboundMessageRequest` or `OutboundMessageResponse` classes.

### Transport Protocol

The transport protocol is implemented in a loop performing the following.

1. Listen for any incoming connections.
2. On connection, read initial bytes into a `TcpHeader` class.
   1. Identify whether it is a request or response, and what the request ID is. A response will carry the same ID.
   2. Identify the version of the sender, used in case compatibility decisions may change the response.
   4. Identify any thread context headers.
3. An `OutboundMessageRequest` or `OutboundMessageResponse` subclass is instantiated, picking up reading the input stream.
   1. For requests, this instance reads the features and the name of the Transport Action identifying the `TransportMessage` handler.
   2. For responses, there is no additional information read, as the request ID identifies the handler expecting the response.
4. Following the fixed and variable headers, the content of the `TransportRequest` or `TransportResponse` is available for reading from the input stream. This stream and the instance created in the previous step are passed to the handler for the request (based on the action name) or response (based on the request ID).
5. Handlers parse the request from the input stream, perform whatever actions they need to perform, and then return a response as an outbound stream, matching the request ID in the case of requests. This outbound stream is then sent back to OpenSearch.
6. Sometimes the actions a handler performs are to send transport requests back to OpenSearch, where a similar loop will handle the request and return a response.
