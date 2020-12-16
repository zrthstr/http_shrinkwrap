#!/usr/bin/env python3

import sys
import os
import copy
import hashlib
#import pprint
import fileinput
import uncurl
import curlify

from requests import Request, Session, structures
from loguru import logger as log


# read curl commands form stdin
# get rid of all curl paramters that dont seem to make a difference
# write curl command back to stdout
#
# limitation: only a small subset of curl is supported,
# the parameters that come from chrome > copy_as_curl...


# what's next?
#  condense cookies?


def send(seq, log_msg="headers"):
    resp = session.send(seq)
    log.trace(
        f"{log_msg}: {len(seq.headers)}, reply len: {len(resp.text)} status {resp.status_code}"
    )
    return resp.status_code, len(resp.text), hashlib.sha256(resp.text.encode('utf-8')).hexdigest()


def parse(line):
    #log.info(f"Processing line {line}")
    context = uncurl.parse_context(line)
    ## uncurl doesn't guarantee an url scheme while curlify insists on having one
    if not context.url.startswith("http"):
        context = context._replace(url="http://" + context.url)
    req = Request(
        context.method.upper(), context.url, headers=context.headers, data=context.data
    )
    return req


def is_same_without(prep, without, full_status_code, full_len, full_hash):
    # print(dir(prep.headers))
    one_less = copy.deepcopy(prep)
    del one_less.headers[without]

    new_status, new_len, new_hash = send(one_less)
    # print(prep.headers)
    #if new_status == full_status_code and new_len == full_len:
    if new_status == full_status_code and new_hash == full_hash:
        return False
    return True


def triage(prep_full, full_status_code, full_len, full_hash):
#def triage(prep_full, _ , full_len):
    header_count = len(prep_full.headers)
    if len(prep_full.headers) == 1:
        return prep_full

    log.debug(f"Starting triage with: {header_count} headers")
    # for h in range(0, header_count):

    obsolete_headers = structures.CaseInsensitiveDict()
    needed_headers = structures.CaseInsensitiveDict()
    for headder_name, headder_value in prep_full.headers.items():
        if is_same_without(prep_full, headder_name, full_status_code, full_len, full_hash):
            log.debug(f"Found needed headder: {headder_name, headder_value}")
            needed_headers[headder_name] = headder_value
        else:
            log.debug(f"Found obsolete headder: {headder_name, headder_value}")
            obsolete_headers[headder_name] = headder_value
            # del header

    #log.debug(f"Needed: { pprint.pformat(dict(needed_headers), width=9999, indent=4)}")
    #log.debug(f"Obsolete: {pprint.pformat(dict(obsolete_headers), width=-1, indent=4)}")

    prep_full.headers = needed_headers
    return prep_full

def condense(prep_full, full_status_code, full_len, full_hash):
    max_user_agent_len = 15
    org_user_agent = prep_full.headers["user-agent"]
    log.debug(f'condensing User-Agent: {org_user_agent}')
    if " " in org_user_agent.lower():
        prep_full.headers["user-agent"] = org_user_agent.split()[0]
    elif len(org_user_agent) > max_user_agent_len:
        prep_full.headers["user-agent"] = org_user_agent[0:max_user_agent_len]
    else:
        # no change, no test needed
        return prep_full

    # make sure condensing has no effect
    new_status, new_len, new_hash = send(prep_full, log_msg="condenseing")
    #if (new_status, new_len) != (full_status_code, full_len):
    if (new_status, new_hash) != (full_status_code, full_hash):
        prep_full.headers["user-agent"] = org_user_agent
    return  prep_full


def process(line):
    req = parse(line)
    global session
    #global full_status
    #global full_len

    session = Session()
    prep_full = req.prepare()
    prep_plain = copy.deepcopy(prep_full)
    prep_plain.headers = structures.CaseInsensitiveDict()

    log.debug("Probing full request")
    full_status_code, full_len, full_hash = send(prep_full)
    log.debug("Probing plain request")
    plain_status_code, plain_len, plain_hash = send(prep_plain)

    if not full_status_code == 200:
        log.error(f"Supplied curl command not exiting with status 200: {full_status_code}")
        sys.exit()

    if full_len == 0:
        log.warning("Original requests reply has length 0. Continuing")

    #if plain_status_code == full_status_code and full_len == plain_len:
    if plain_status_code == full_status_code and full_hash == plain_hash:
        log.debug("Done. All headers have no effect")
        return prep_plain

    log.debug("Some Headders appear relevant. Starting triage")
    prep_minimum = triage(prep_full, full_status_code, full_len, full_hash)


    if 'user-agent' in prep_minimum.headers:
        prep_minimum = condense(prep_minimum, full_status_code, full_len, full_hash)

    return prep_minimum


if __name__ == "__main__":

    # for fc + vim usecase:
    # detect if calling process is editor
    # set non verbose logging then

    if os.readlink("/proc/%s/exe" % os.getppid()).endswith(("/vi", "/vim")):
        for log_level in ["DEBUG", "INFO", "WARN"]:
            log.disable(log_level)

    for curl_line in fileinput.input():
        log.debug(f"Processing curl: {curl_line}")
        request_obj = process(curl_line)
        print(curlify.to_curl(request_obj))

        # try:
        #    process(line)
        # except:
        #    print("line failed: ", line)
