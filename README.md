### http_shrinkwrap
shrinks curl command to minimal form, getting rid of all http headers that have no apparent effect and shortening cookies and user agent

### example
see `make test_external`

## usage
### usecase plain

### usecase with fc & vim
in Chrome/Mozilla dev tools > rightclick > "copy request as curl" > pip to ./hsw.py; echo COMMAND | ./hsw.py

`export EDITOR="vim"`
in Chrome/Mozilla dev tools > "copy request as curl" > paste and execute curl command in terminal
then run `fc` > now inside vim run `:%! ./hsw.py` > `:w outfile`
 
## install
tbd
