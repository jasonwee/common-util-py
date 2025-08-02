## common-util-py
Common utilities in Python

## How to install
The following commands show how to install `common-util-py` using pip within a Python virtual environment. To see which versions of Python are supported by `common-util-py`, see (here)[#tested-installation-via-pypi-on-the-following-python-versions].
```sh
$ python3 -m venv py313_env
$ source py313_env/bin/activate
$ pip install .[dev]
$ # or
$ virtualenv --python=/usr/bin/python3 py39_env
$ source env_py39/bin/activate
$ pip install .
$ # or
$ python3.8 -m venv env_py38
$ source env_py38/bin/activate
$ pip install .
```

## How to build
To create a source distribution, run the following commands:
```sh
$ source py313_env/bin/activate
$ python3 setup.py --help-commands
$ python3 setup.py sdist
```

## How to test
Initially we were using `nosetests` and have since migrated to `pytest`.
```sh
$ # deprecated
$ # python setup.py test
$ # python setup.py nosetests
$ # nose is replace by pytest since python3.13
$ pytest
```

read more [here](https://nose.readthedocs.io/en/latest/setuptools_integration.html)


* https://www.codingforentrepreneurs.com/blog/pipenv-virtual-environments-for-python/
* https://packaging.python.org/
* https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

## How to upload to PyPI (Python Package Index)
First, build a source distribution and then install the `twine` package.
```sh
$ python setup.py sdist
$ pip install twine
```
Then, use twine to upload the package to PyPI.
```sh
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
or
```sh
$ twine upload --config-file ~/.pypirc -r testpypi dist/common_util_py-0.0.1.tar.gz
```

## Test install
Install from Test PyPI
```sh
$ pip install --index-url https://test.pypi.org/simple/ common-util-py
```
Install from Local Distribution.
```sh
$ pip install dist/common_util_py-<version>.tar.gz
```

## Legacy
To generate `requirements.txt` and `requirements-dev.txt` from `pyproject.toml`, run the following command.
```
pip install pip-tools
pip-compile --extra dev pyproject.toml -o requirements-dev.txt
pip-compile pyproject.toml -o requirements.txt
```

## Tested installation via PyPI on the following Python versions:
| Python Version  | tested installed  |
| --------------- |:-----------------:|
| 3.9             | Yes               |
| 3.10            | Yes               |
| 3.11            | Yes               |
| 3.12            | Yes               |
| 3.13            | Yes               |
| 3.14            | Upcoming          |


