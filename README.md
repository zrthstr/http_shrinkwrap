# http_shrinkwrap - Minimizes curl HTTP commands
## In a nutshell
http_shrinkwrap is a command line tool that removes all obsolete HTTP headers from a curl HTTP request.
* All headers that have no apparent effect on the response obtained from the webserver are removed.
* Long Cookies and some other header values are also shortened.  

Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for minimizing the recreated browser requests in your shell.
The tool is written in python and based on [uncurl](https://github.com/spulec/uncurl).


## Example
### Example ipinfo
turns this:

```bash
curl 'https://ipinfo.io/' -H 'authority: ipinfo.io' -H 'cache-control: max-age=0' -H 'dnt: 1' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/534.16' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'sec-fetch-site: none' -H 'sec-fetch-mode: navigate' -H 'sec-fetch-user: ?1' -H 'sec-fetch-dest: document' -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5' -H 'sec-gpc: 1' --compressed
```

into this:

```bash
curl -X GET -H 'user-agent: Mozilla/5.0' https://ipinfo.io/
```

### Example heise.de
turns this:

```bash
curl 'https://www.heise.de/'   -H 'authority: www.heise.de'   -H 'cache-control: max-age=0'   -H 'dnt: 1'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/137.36'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-fetch-site: none'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-user: ?1'   -H 'sec-fetch-dest: document'   -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5'   -H 'cookie: wt_nv_s=1; wt3_sid=%3B288689636920174%3B589751618140993; wt_ttv2_e_288689636920174=meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; wt_ttv2_c_288689636920174=meldung.newsticker.bottom.kommentarelesen*4428549%3AAntergos-Entwickler%20stellen%20Linux-Projekt%20ein**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4432329%3AEuropa-Wahl%3A%20Schwere%20Schlappe%20f%C3%BCr%20deutsche%20Koalitionsparteien%2C%20Erfolge%20f**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4436209%3AHuawei-Konflikt%3A%20China%20k%C3%BCndigt%20eigene%20schwarze%20Liste%20an**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; volumeControl_volumeValue=100; wt_nv=1; wt_ttv2_s_288689636920174=9700; wt_ttv2_s_288689636920174=9700; wt3_eid=%3B288689636920174%7C2155707251500935604%232159741754555500039%3B589751618140993%7C2155796048217456639%232155796801880162886'   -H 'sec-gpc: 1'   -H 'if-modified-since: Wed, 18 Nov 2020 21:57:08 GMT'   --compressed
```

into this:

```bash
curl -X GET https://www.heise.de/
```

## Usage
There are three main ways to run `http_shrinkwrap`
* By passing a `file` as an argument
* Via piping a curl command from `stdin`
* By calling `http_shrinkwrap` from insde `vim` (or `fc`)

### Via file
	http_shrinkwrap file_containing_curl_cmd

eg:
* in Chrome/Mozilla dev tools > "copy request as curl" & paste to some_file
* `http-shrinkwrap some_file`

### Via stdin
pipe curl command to `http-shrinkwrap`
eg:
* in Chrome/Mozilla dev tools > "copy request as curl"
* `echo "curl http://foo.com -H 'some thing'" | http-shrinkwrap`

Note:
* wrap the curl command in double quotes
* this will not work if the curl command has single and double quotes or other sepcial chars. Use the file method in these cases.


### From fc & vim
given `export EDITOR="vim"`

* in Chrome/Mozilla dev tools > "copy request as curl"
* paste and execute curl command in terminal
* run `fc`
* now inside vim run `:%! http-shrinkwrap`
* then save output if needed `:w outfile_name`


## Install
	pip3 install -i https://test.pypi.org/simple/ http-shrinkwrap


## Run without install
	git clone https://github.com/zrthstr/http_shrinkwrap
	cd http_shrinkwrap
	pip install -r requirements.txt
	
	echo 'some curl cmd ' | python -m http_shrinkwrap.bin
	# or
	python -m http_shrinkwrap.bin some_file_containing_a_curl_cmd


## Development

### Debugging
`export DEBUG=TRUE`

### Testing
	make test

### License
Apache License 2.0

### Develpement
Written by zrth1k@gmail.com
Thanks to [Lars Wirzenius](https://liw.fi/readme-review/) for reviewing the README!
