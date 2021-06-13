
#########
## env ##
#########

setup-environ:
	#sudo apt-get install python3 pip
	#sudo pip3 install pipenv
	pipenv install
	pipenv shell

environ:
	pipenv shell


##########
## test ##
##########

test: test_external test_internal

test_external:
	#cd test && ./test_external.sh
	#cd http_shrinkwrap && ../test/test_external.sh
	./test/test_external.sh

test_internal:
	#cd test && ./test_internal.sh
	#cd http_shrinkwrap && ../test/test_internal.sh
	./test/test_internal.sh


###########
## build ##
###########

build:
	python setup.py sdist bdist_wheel

# test upload
upload:
	twine upload -r testpypi dist/*

install_from_pypi_test:
	pip3 install -i https://test.pypi.org/simple/ http-shrinkwrap
#https://test.pypi.org/project/http-shrinkwrap/

bump:
	bumpversion --config-file .bumpversion.cfg patch

clean:
	rm -rf dist build http_shrinkwrap.egg-info http_shrinkwrap/__pycache__

install_from_tgz:
	sudo pip3 install dist/http_shrinkwrap-0.0.*.tar.gz

uninstall:
	sudo pip3 uninstall -y http-shrinkwrap

#release: clean bump biild upload # and git push

##############
## e2e test ##
##############

reinstall: uninstall clean build install_from_tgz test_system_version

test_system_version:
	DEBUG=TRUE echo 'curl https://www.heise.de -H "fff: foo" -H "fofoof: foofofo"'  | http-shrinkwrap


#to be removed
true:
	echo YESYESYEYSEYS
