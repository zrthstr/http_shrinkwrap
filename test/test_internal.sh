#!/usr/bin/bash


HOST="http://127.0.0.1"


function test_0 {
(
timeout 2 ./test_server.py 0&
sleep 1

cat <<EOF
curl "${HOST}:${1}" \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-gpc: 1' \
  --compressed
EOF
) | ../hsw.py
}

# heise
function ipinfo {
	(
cat <<EOF
curl 'https://ipinfo.io/' \
  -H 'authority: ipinfo.io' \
  -H 'cache-control: max-age=0' \
  -H 'dnt: 1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/534.16' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5' \
  -H 'sec-gpc: 1' \
  --compressed
EOF
) | ../hsw.py
}


test_0 8000
