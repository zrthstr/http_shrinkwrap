#!/usr/bin/env bash

set -e
set -o pipefail   # Unveils hidden failures
set -o nounset    # Exposes unset variables

#EXEC="python3 ../http_shrinkwrap/bin.py"
EXEC="poetry run python3 -m http_shrinkwrap.bin"

HOST="http://127.0.0.1:8000"
TIMEOUT=12
export DEBUG=TRUE


function test_some {
	### GET request with some needed and some obsolete headers
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' ${HOST}/some"
	out=$(echo "${SHOULD} -H 'Not-Needed: Something' --compressed" \
		| $EXEC )
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "some_headers test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_none {
	### GET request with only obsolete headers
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET ${HOST}/static"
	out=$(echo "${SHOULD} -H 'Not-Needed-0: Is-0' -H 'Not-Needed-1: Is-1' -H 'Not-Needed-2: Something' --compressed" \
		| $EXEC )
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "none_needed test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_useragent {
	### GET request with obsolete User-Agent
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'User-Agent: Mozilla/5.0' ${HOST}/useragent"
	out=$(echo "${SHOULD} -H 'User-Agent: Mozilla/5.0 UNNECECARY_UNNECECARY_UNNECECARY_UNNECECARY_UNNECECARY'" \
		| $EXEC )
	echo out: $out
	[[ "${out}" == "${SHOULD}" ]] || (echo "user_agent test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_random {
	### Non deterministic check that should trigger “Flip Flop Detection”
	echo "[*] Running test: ${FUNCNAME[0]}"
	RET_SHOULD="3"
	echo "curl -X GET -H 'Needed-1: Is-1' -H 'Needed-0: Is-0'  ${HOST}/random" \
	| $EXEC && true
		[[ $? -eq ${RET_SHOULD} ]] || (echo "Flip flop test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_null {
	### GET request returning empty reply when Needed header is present
	### else returns "NOPE"
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'Needed-0: Is-0' ${HOST}/null"
	out=$(echo "${SHOULD} -H 'User-Agent: NOTNEEDED'" \
		| $EXEC )
	[[ "${out}" == "${SHOULD}" ]] || (echo "null test failed"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_some_post {
	### GET request with some needed and some obsolete headers
	echo "[*] Running test: ${FUNCNAME[0]}"
	#SHOULD="curl -X POST --data 'some_data' -H 'Needed-0: Is-0' ${HOST}/some"
	SHOULD="curl -X POST -H 'Content-Length: 9' -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' -d some_data ${HOST}/some"
	out=$(echo "${SHOULD} -H 'User-Agent: NOTNEEDED' -H 'Foo: foo'" \
		| $EXEC )
	[[ "${out}" == "${SHOULD}" ]] || (echo "${FUNCNAME[0]} failed......"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_cache_304_flag {
	### GET request. Reply with 304 if If-None-Match or If-Modified-Since present
	### in this test hsw gets called with the option to bust caches
	CMD_FLAGS="--bust"
	echo "[*] Running test: ${FUNCNAME[0]}"
	SHOULD="curl -X GET -H 'Needed-0: Is-0' ${HOST}/get_304"
	out=$(echo "${SHOULD} -H 'User-Agent: NOTNEEDED'" \
		| $EXEC $CMD_FLAGS )
	[[ "${out}" == "${SHOULD}" ]] || (echo "${FUNCNAME[0]} failed......"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function test_cache_304 {
	### GET request. Reply with 304 if If-None-Match or If-Modified-Since present
	### in this test hsw is NOT called with the command line option to bust caches
	### the server respods with 304
	echo "[*] Running test: ${FUNCNAME[0]}"
	RET_SHOULD="48"
	echo "curl -H 'User-Agent: NOTNEEDED' -H 'Needed-0: Is-0' -H 'If-None-Match: 33a64df5' ${HOST}/get_304" \
	| $EXEC && true
	[[ $? -eq "${RET_SHOULD}" ]] || (echo "${FUNCNAME[0]} failed......"; exit 1)
	echo "[*] Test ${FUNCNAME[0]} passed!"
}

function start_test_server {
	echo "[*] Starting testing server with timeout: $1"
	poetry run timeout ${1} ./test/test_server.py & 1>&2
	sleep 0.5
}


start_test_server $TIMEOUT
test_useragent
test_null
test_some_post
test_random
test_cache_304_flag
test_cache_304
test_none
test_some
