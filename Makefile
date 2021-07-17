#########
## env ##
#########

env:
	poetry install


##########
## test ##
##########

test: test_external test_internal

test_external:
	./test/test_external.sh

test_internal:
	./test/test_internal.sh


#########
## dev ##
#########

publish-testing:
	poetry publish -r https://test.pypi.org/legacy/

build_config:
	poetry config repositories.testpypi https://test.pypi.org/legacy/Q
	# see https://blog.frank-mich.com/python-poetry-1-0-0-private-repo-issue-fix/?utm_source=pocket_mylist
	# poetry config pypi-token.pypi my-SECRET-token

install_from_repo:
	pip3 install -U git+https://github.com/zrthstr/http_shrinkwrap.git@cachebuster-304
	#pip3 install -e . 
	#pip3 install -e http_shrinkwrap
	#pip3 install --no-binary http_shrinkwrap==0.1.0 -e .

install_from_pypi_test:
	pip3 install -U -i https://test.pypi.org/simple/ http-shrinkwrap
#https://test.pypi.org/project/http-shrinkwrap/

install_from_tgz:
	#sudo pip3 install dist/http_shrinkwrap-0.0.*.tar.gz
	pip3 install -U dist/http_shrinkwrap-*.tar.gz



###########
## build ##
###########



build:
	poetry build

publish-prod:
	poetry publish

bump:
	bumpversion --config-file .bumpversion.cfg patch

clean:
	rm -rf dist build http_shrinkwrap.egg-info http_shrinkwrap/__pycache__

uninstall:
	sudo pip3 uninstall -y http-shrinkwrap
	pip3 uninstall -y http-shrinkwrap


#release: clean bump biild upload # and git push

##############
## e2e test ##
##############

reinstall: uninstall clean build install_from_tgz test_system_version
#reinstall: uninstall clean build install_from_pypi_test test_system_version

test_system_version:
	DEBUG=TRUE echo 'curl https://www.heise.de -H "fff: foo" -H "fofoof: foofofo"'  | hsw

