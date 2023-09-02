- [Forking and Cloning](#forking-and-cloning)
- [Building](#building)
  - [Install Prerequisites](#install-prerequisites)
    - [Pyenv](#pyenv)
    - [Python 3.9](#python-39)
    - [Poetry](#poetry)
  - [Install Dependencies](#install-dependencies)
  - [Run Tests](#run-tests)
  - [Cleanup Code](#cleanup-code)

## Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.

## Building

This project contains a collection of tools to build, test and release `opensearch_sdk_py`.

### Install Prerequisites

#### Pyenv

Use pyenv to manage multiple versions of Python. This can be installed with [pyenv-installer](https://github.com/pyenv/pyenv-installer) on Linux and MacOS, and [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) on Windows.

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

#### Python 3.9

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

#### Poetry

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

```
poetry run pytest -v
```

### Cleanup Code

The [lint workflow](.github/workflows/lint.ml) runs `flake8`. Make sure `poetry run flake8 .` is clean before making pull requests. Use the following to auto-clean and auto-format.

```
poetry run isort .
poetry run black .
poetry run autoflake .
```
