## common-util-py
Common utilities in Python

## How to install
The following commands show how to install `common-util-py` using pip within a Python virtual environment. To see which versions of Python are supported by `common-util-py`, see (here)[#tested-installation-via-pypi-on-the-following-python-versions].
```sh
$ python3 -m venv py313_env
$ source py313_env/bin/activate
$ pip install .
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
```sh
$ python setup.py --help-commands
$ python setup.py sdist
```

## How to test
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
```sh
$ python setup.py sdist
$ pip install twine
```

## Commands to upload to the PyPI test repository
```sh
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
or
```sh
$ twine upload --config-file ~/.pypirc -r testpypi dist/common_util_py-0.0.1.tar.gz
```

## Test install
```sh
$ pip install --index-url https://test.pypi.org/simple/ common-util-py
$ # or local install for quick test
$ pip install dist/common_util_py-<version>.tar.gz
```

## Tested installation via PyPI on the following Python versions:
| python        | tested installed  |
| ------------- |:-----------------:|
| 3.9           | yes               |
| 3.10          | yes               |
| 3.11          | yes               |
| 3.12          | yes               |
| 3.13          | yes               |
| 3.14          | incoming          |

## Command to upload to the PyPI repository
```sh
$ twine upload dist/*
$ pip install common-util-py
```
