

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
