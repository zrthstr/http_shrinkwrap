#!/usr/bin/env python3

import fileinput
import uncurl
import curlify
import sys
import copy

from requests import Request, Session, structures
from loguru import logger as log


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


def send(seq):
    # print(seq.headers)
    resp = s.send(seq)
    # log.info(
    #    f"headers: {len(seq.headers)}, reply len: {len(resp.text)} status {resp.status_code}"
    # )
    return resp.status_code, len(resp.text)


def parse(line):
    log.info(f"Processing line {line}")
    context = uncurl.parse_context(line)
    ## uncurl doesn't guarantee an url scheme while curlify insists on having one
    if not context.url.startswith("http"):
        # context.url = "http://" + context.url ## context is RO...
        context = context._replace(url="http://" + context.url)
    req = Request(
        context.method.upper(), context.url, headers=context.headers, data=context.data
    )
    return req


def is_same_without(prep, without):
    # print(dir(prep.headers))
    one_less = copy.deepcopy(prep)
    del one_less.headers[without]

    new_status, new_len = send(one_less)
    # print(prep.headers)
    if new_status == new_status and new_len == full_len:
        return False
    return True


def triage(prep_full, full_status_code, full_len):
    header_count = len(prep_full.headers)
    if len(prep_full.headers) == 1:
        return prep_full

    log.info(f"Starting triage with: {header_count} headers")
    # for h in range(0, header_count):

    obsolete_headers = structures.CaseInsensitiveDict()
    needed_headers = structures.CaseInsensitiveDict()
    for k, v in prep_full.headers.items():
        if is_same_without(prep_full, k):
            log.info(f"Found needed headder: {k, v}")
            needed_headers[k] = v
        else:
            log.info(f"Found obsolete headder: {k, v}")
            obsolete_headers[k] = v
            # del header

    import pprint

    log.debug(f"Needed:")
    pprint.pprint(dict(needed_headers), width=9999, indent=4)

    log.debug(f"Obsolete:")
    pprint.pprint(dict(obsolete_headers), width=-1, indent=4)

    prep_full.headers = needed_headers
    return prep_full


def process(line):
    req = parse(line)
    global s
    global full_status
    global full_len
    s = Session()
    prep_full = req.prepare()
    prep_plain = copy.deepcopy(prep_full)
    prep_plain.headers = structures.CaseInsensitiveDict()

    log.info("Probing full request")
    full_status_code, full_len = send(prep_full)
    log.info("Probing plain request")
    plain_status_code, plain_len = send(prep_plain)

    if not full_status_code == 200:
        log.error("Aborting: Original query not of status 200: " + full_status_code)
        #### must thest if this end the program
        #### if not do so
        #### sys.exit()

    elif plain_status_code == full_status_code and full_len == plain_len:
        log.info("Done. Headers have no effect", dir(prep_plain))
        return prep_plain

    else:
        log.info("Some Headders needed. Starting search")
        prep_minimum = triage(prep_full, full_status_code, full_len)
        return prep_minimum


if __name__ == "__main__":
    for line in fileinput.input():
        request_obj = process(line)
        print(curlify.to_curl(request_obj))
        # try:
        #    process(line)
        # except:
        #    print("line failed: ", line)
