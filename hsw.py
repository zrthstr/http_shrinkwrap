#!/usr/bin/env python3

import fileinput
import uncurl
import curlify

from requests import Request, Session, structures


# read curl commands form stdin
# get rid of all curl paramters that dont seem to make a difference
# write curl command back to stdout
#
# limitation: only a small subset of curl is supported, the parameters that come from chrome > copy_as_curl...


# TODO:
# start with http header diet
#
# next:
# check if unculr treats cookie as regular header
# clean error on non http(s)
#
# what else?
# put data on diet?
# remove referrer?


def send(s, seq):
    #print("header count: ", len(context.headers))
    #print("text len: ", len(resp.text))
    #print(resp.status_code)
    resp = s.send(seq)
    return resp.status_code, len(resp.text)


def process(line):
    print(line)
    curl_in = uncurl.parse(line)
    print(curl_in)
    context = uncurl.parse_context(line)
    print(context)
    #print(dir(context))

    ## uncurl doesn't guarantee an url scheme while curlify insists on having one
    if not context.url.startswith("http"):
        #context.url = "http://" + context.url ## context is RO...
        context = context._replace(url="http://"+context.url)

    essential_headers = []

    s = Session()

    req_full = Request(context.method.upper(), context.url, headers=context.headers, data=context.data)

    prep_full = req_full.prepare()
    prep_plain = prep_full
    #print(dir(prep_full))
    #print(type(prep_full.headers))
    #prep_plain.headers = {}
    prep_plain.headers = structures.CaseInsensitiveDict()

    #req_plain = Request(context.method.upper(), context.url, data=context.data)


    full_status_code, full_resp_text = send(s, prep_full)
    plain_status_code, plain_resp_text = send(s, prep_plain)

    print("full_status_code", full_status_code)
    print("full_resp_text", full_resp_text)
    print("plain_status_code", plain_status_code)
    print("plain_resp_text", plain_resp_text)

    if not full_status_code == 200:
        ## this is not good ..
        raise("Aborting: Original query not returning http 200 > "+full_status_code)

    if plain_status_code == full_status_code and full_resp_text == plain_resp_text:
        ## nice, no headders needed ...
        return prep_plain
        print("XXXXXXXXXXXXx",dir(prep_plain))

    else:
        # bla bla bla this is not done ..
        print("NOOOOOOOOOOO")
        import sys
        sys.exit()


for line in fileinput.input():
    request_obj =  process(line)
    print(curlify.to_curl(request_obj))
    #try:
    #    process(line)
    #except:
    #    print("line failed: ", line)
