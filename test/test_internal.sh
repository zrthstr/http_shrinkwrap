#!/usr/bin/bash

set -e

HOST="http://127.0.0.1:8000"
TIMEOUT=12


function test_some {
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' ${HOST}/some"
	out=$(echo "${SHOULD} -H 'Not-Needed: Something' --compressed" \
		| ../hsw.py)
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "some_headers test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_none {
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET ${HOST}/static"
	out=$(echo "${SHOULD} -H 'Not-Needed-0: Is-0' -H 'Not-Needed-1: Is-1' -H 'Not-Needed-2: Something' --compressed" \
		| ../hsw.py)
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "none_needed test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_useragent {
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'User-Agent: Mozilla/5.0' ${HOST}/useragent"
	out=$(echo "${SHOULD} -H 'User-Agent: Mozilla/5.0 UNNECECARY_UNNECECARY_UNNECECARY_UNNECECARY_UNNECECARY'" \
		| ../hsw.py)
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "user_agent test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_random {
	echo "[*] Running test: ${FUNCNAME[0]}"
	RET_SHOULD="3"
	echo "curl -X GET -H 'Needed-1: Is-1' -H 'Needed-0: Is-0'  ${HOST}/random" \
	| ../hsw.py && true
		[[ $? -eq ${RET_SHOULD} ]] || (echo "Flip flop test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_null {
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'Needed-0: Is-0' ${HOST}/null"
	out=$(echo "${SHOULD} -H 'User-Agent: NOTNEEDED'" \
		| ../hsw.py)
	[[ "${out}" == "${SHOULD}" ]] || (echo "null test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_some_post {
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X POST --data 'some_data' -H 'Needed-0: Is-0' ${HOST}/null"
	out=$(echo "${SHOULD} -H 'User-Agent: NOTNEEDED'" \
		| ../hsw.py)
	[[ "${out}" == "${SHOULD}" ]] || (echo "null test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function start_test_server {
	echo "[*] Starting testing server with timeout: $1"
	timeout ${1} ./test_server.py & 1>&2
	sleep 0.5
}


start_test_server $TIMEOUT
test_useragent
test_null
test_none
test_some
test_some_post
test_random


