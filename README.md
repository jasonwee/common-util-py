# common-util-py
common utilies in python


how to install
===========
```sh
virtualenv --python=/usr/bin/python3 py39_env
or
python3.8 -m venv env_py38
source env_py38/bin/activate
pip install .
```

how to build
===========
```sh
$ python setup.py --help-commands
$ python setup.py sdist
```

how to test
===========
```sh
$ python setup.py test
$ python setup.py nosetests
```

read more [here](https://nose.readthedocs.io/en/latest/setuptools_integration.html)


https://www.codingforentrepreneurs.com/blog/pipenv-virtual-environments-for-python/
https://packaging.python.org/
https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

how to upload to pypi
===========
python setup.py sdist
pip install twine

# commands to upload to the pypi test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
or
twine upload --config-file ~/.pypirc -r testpypi dist/common_util_py-0.0.1.tar.gz

# test install
pip install --index-url https://test.pypi.org/simple/ common-util-py

# command to upload to the pypi repository
twine upload dist/*
pip install common-util-py

