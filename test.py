#!/usr/bin/env python3

# testing cases
#
# * return same for any request
# * return other for any other but original request
# * one headder needed
# * all but one headder needed
#
# * insensitive user agent
# * sesitive user agent
# *  .. ?

#from http.server import HTTPServer, BaseHTTPRequestHandler,  SimpleHTTPRequestHandler

import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run(arg, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
#def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    port = 8000 + arg
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print(dir(httpd))
    httpd.handle_request()

    #httpd.process_request()
    #httpd.serve_forever()

def usage():
    print("error:  TBD")
    print(f"example: {sys.argv[0]} 0 1 2 [testcase]")
    print(f"example: {sys.argv[0]} 3 4")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    for arg in sys.argv[1:]:
        try:
            arg = int(arg)
            assert -1 < arg < 5
            #assert -1 < arg < len(testcases)
        except:
            print(f"skipping invalid testcase: {arg}")
            continue
        run(arg)
