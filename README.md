## common-util-py
common utilities in python

## how to install

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

## how to build
```sh
$ python setup.py --help-commands
$ python setup.py sdist
```

## how to test
```sh
$ python setup.py test
$ python setup.py nosetests
```

read more [here](https://nose.readthedocs.io/en/latest/setuptools_integration.html)


https://www.codingforentrepreneurs.com/blog/pipenv-virtual-environments-for-python/
https://packaging.python.org/
https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

## how to upload to pypi
```sh
$ python setup.py sdist
$ pip install twine
```

## commands to upload to the pypi test repository
```sh
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
or
```sh
$ twine upload --config-file ~/.pypirc -r testpypi dist/common_util_py-0.0.1.tar.gz
```

## test install
```sh
$ pip install --index-url https://test.pypi.org/simple/ common-util-py
$ # or local install for quick test
$ pip install dist/common_util_py-<version>.tar.gz
```

## tested install via pypi on the following py version
| python        | tested installed  |
| ------------- |:-----------------:|
| 3.9           | yes               |
| 3.10          | yes               |
| 3.11          | yes               |
| 3.12          | yes               |

## command to upload to the pypi repository
```sh
$ twine upload dist/*
$ pip install common-util-py
```
