
test: test_external test_internal

test_external:
	cd test && ./test_external.sh

test_internal:
	cd test && ./test_internal.sh
