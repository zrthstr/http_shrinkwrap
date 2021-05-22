

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
create_dist:
	python setup.py sdist bdist_wheel

# test upload
upload:
	twine upload -r testpypi dist/*

## pip install -i https://test.pypi.org/simple/ http-shrinkwrap
## https://test.pypi.org/project/http-shrinkwrap/

bump:
	bumpversion --config-file .bumpversion.cfg patch

clean:
	rm -rf dist build http_shrinkwrap.egg-info
