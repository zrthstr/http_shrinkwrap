

setup-environ:
	#sudo apt-get install python3 pip
	#sudo pip3 install pipenv
	pipenv install
	pipenv shell

environ:
	pipenv shell

test: test_external test_internal

test_external:
	cd test && ./test_external.sh

test_internal:
	cd test && ./test_internal.sh

# create dist
build:
	python setup.py sdist bdist_wheel

# test upload
upload:
	twine upload -r testpypi dist/*

## pip install -i https://test.pypi.org/simple/ http-shrinkwrap
## https://test.pypi.org/project/http-shrinkwrap/

bump:
	bumpversion --config-file .bumpversion.cfg patch

clean:
	rm -rf dist build http_shrinkwrap.egg-info http_shrinkwrap/__pycache__

test_install:
	sudo pip3 install dist/http_shrinkwrap-0.0.*.tar.gz

test_uninstall:
	sudo pip3 uninstall -y http-shrinkwrap

reinstall: test_uninstall clean build test_install

test_local:
	DEBUG=TRUE echo 'curl https://www.heise.de -H "fff: foo" -H "fofoof: foofofo"'  | http-shrinkwrap
