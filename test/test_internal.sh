#!/usr/bin/bash


HOST="http://127.0.0.1:8000"
TIMEOUT=12


function test_0 {
#echo "curl ${HOST}/some -H 'sec-fetch-site: none' -H 'sec-fetch-user: ?1' --compressed" \
echo "curl ${HOST}/some -H 'Needed-0: Is-0' -H 'Needed-1: Is-1' -H 'Not-Needed: Something' --compressed" \
 | ../hsw.py
}


function start_test_server {
	timeout ${1} ./test_server.py & 1>&2
	sleep 0.5
}


start_test_server $TIMEOUT
test_0
