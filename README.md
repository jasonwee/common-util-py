## common-util-py
common utilities in python

## How to install

```sh
$ python3 -m venv py312_env
$ source py312_env/bin/activate
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

## How to upload to pypi
```sh
$ python setup.py sdist
$ pip install twine
```

## Commands to upload to the pypi test repository
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

## Tested install via pypi on the following py version
| python        | tested installed  |
| ------------- |:-----------------:|
| 3.9           | yes               |
| 3.10          | yes               |
| 3.11          | yes               |
| 3.12          | yes               |
| 3.13          | yes               |

## Command to upload to the pypi repository
```sh
$ twine upload dist/*
$ pip install common-util-py
```
