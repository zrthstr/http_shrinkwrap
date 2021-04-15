# http_shrinkwrap - Shrinks curl HTTP requests commands to their minimal form by removing obsolete HTTP headers
# In a nutshell
http_shrinkwrap is a cli tool that allows you to remove all HTTP headers that have no effect on the response obtained from the webserver.
Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for minimizing the recreated browser requests in your shell.
The tool is written in python an based on [uncurl](https://github.com/spulec/uncurl).


## Example
### Example ipinfo
turns this:

	curl 'https://ipinfo.io/'   -H 'authority: ipinfo.io'   -H 'cache-control: max-age=0'   -H 'dnt: 1'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/534.16'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-fetch-site: none'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-user: ?1'   -H 'sec-fetch-dest: document'   -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5'   -H 'sec-gpc: 1'   --compressed

into this:

	curl -X GET -H 'user-agent: Mozilla/5.0' https://ipinfo.io/
### example heise.de
turns this:

	curl 'https://www.heise.de/'   -H 'authority: www.heise.de'   -H 'cache-control: max-age=0'   -H 'dnt: 1'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.2240.398 Safari/137.36'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-fetch-site: none'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-user: ?1'   -H 'sec-fetch-dest: document'   -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,pt-PT;q=0.7,pt;q=0.6,de;q=0.5'   -H 'cookie: wt_nv_s=1; wt3_sid=%3B288689636920174%3B589751618140993; wt_ttv2_e_288689636920174=meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; wt_ttv2_c_288689636920174=meldung.newsticker.bottom.kommentarelesen*4428549%3AAntergos-Entwickler%20stellen%20Linux-Projekt%20ein**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4432329%3AEuropa-Wahl%3A%20Schwere%20Schlappe%20f%C3%BCr%20deutsche%20Koalitionsparteien%2C%20Erfolge%20f**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4436209%3AHuawei-Konflikt%3A%20China%20k%C3%BCndigt%20eigene%20schwarze%20Liste%20an**meldung.newsticker.bottom*******2*2*~meldung.newsticker.bottom.kommentarelesen*4439526%3ASmart%20Home%3A%20Innenminister%20planen%20Zugriff%20auf%20Daten%20von%20Alexa%20%26%20Co.**meldung.newsticker.bottom*******2*2*; volumeControl_volumeValue=100; wt_nv=1; wt_ttv2_s_288689636920174=9700; wt_ttv2_s_288689636920174=9700; wt3_eid=%3B288689636920174%7C2155707251500935604%232159741754555500039%3B589751618140993%7C2155796048217456639%232155796801880162886'   -H 'sec-gpc: 1'   -H 'if-modified-since: Wed, 18 Nov 2020 21:57:08 GMT'   --compressed

into this:

	curl -X GET https://www.heise.de/

## usage
### from stdin

pipe curl command to `hsw.py`
eg: in Chrome/Mozilla dev tools > "copy request as curl"
`echo COMMAND | ./hsw.py`
eg: `echo "curl http://foo.com -H 'some thing'" | ./hsw.py`

Note:
* wrap the curl command in double quotes
* use "Here documents" if you curl command contains double quotes

### via fc & vi
given `export EDITOR="vim"`

in Chrome/Mozilla dev tools > "copy request as curl" > paste and execute curl command in terminal
then run `fc` > now inside vim run `:%! ./hsw.py` ; then save output if needed `:w outfile_name`


### debug
`export DEBUG=TRUE`

 
## install
tbd
