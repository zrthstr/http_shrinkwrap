#!/usr/bin/bash

set -e

HOST="http://127.0.0.1:8000"
TIMEOUT=12


function test_some {
	SHOULD="curl -X GET -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' http://127.0.0.1:8000/some"
	out=$(echo "curl ${HOST}/some -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' -H 'Not-Needed: Something' --compressed" \
		| ../hsw.py)
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "some_headers test failed"; exit 1)
}

function test_random {
	SHOULD="3"
	echo "curl -X GET -H 'Needed-1: Is-1' -H 'Needed-0: Is-0'  ${HOST}/random" \
	| ../hsw.py
		[[ $? -eq ${SHOULD} ]] || (echo "Flip flop test failed"; exit 1)
}


function start_test_server {
	timeout ${1} ./test_server.py & 1>&2
	sleep 0.5
}


start_test_server $TIMEOUT
test_some
#test_random


