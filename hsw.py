#!/usr/bin/env python3

import sys
import os
import copy
import pprint
import uncurl
import curlify
import fileinput

from requests import Request, Session, structures
from loguru import logger as log


# read curl commands form stdin
# get rid of all curl paramters that dont seem to make a difference
# write curl command back to stdout
#
# limitation: only a small subset of curl is supported, the parameters that come from chrome > copy_as_curl...


# TODO:
# clean error on non http(s)
# add more error handeling
# add more tests
#
# what else?
# shorten needed headers?
#  *useragent
#  *cookies


def send(seq, log_msg="headers"):
    resp = s.send(seq)
    log.trace(
        f"{log_msg}: {len(seq.headers)}, reply len: {len(resp.text)} status {resp.status_code}"
    )
    return resp.status_code, len(resp.text)


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


def is_same_without(prep, without):
    # print(dir(prep.headers))
    one_less = copy.deepcopy(prep)
    del one_less.headers[without]

    new_status, new_len = send(one_less)
    # print(prep.headers)
    if new_status == new_status and new_len == full_len:
        return False
    return True


#def triage(prep_full, full_status_code, full_len):
def triage(prep_full, _ , full_len):
    header_count = len(prep_full.headers)
    if len(prep_full.headers) == 1:
        return prep_full

    log.debug(f"Starting triage with: {header_count} headers")
    # for h in range(0, header_count):

    obsolete_headers = structures.CaseInsensitiveDict()
    needed_headers = structures.CaseInsensitiveDict()
    for k, v in prep_full.headers.items():
        if is_same_without(prep_full, k):
            log.debug(f"Found needed headder: {k, v}")
            needed_headers[k] = v
        else:
            log.debug(f"Found obsolete headder: {k, v}")
            obsolete_headers[k] = v
            # del header

    #log.debug(f"Needed: { pprint.pformat(dict(needed_headers), width=9999, indent=4)}")
    #log.debug(f"Obsolete: {pprint.pformat(dict(obsolete_headers), width=-1, indent=4)}")

    prep_full.headers = needed_headers
    return prep_full

def condense(prep_full, status_code, full_len):
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
    new_status, new_len = send(prep_full, log_msg="condenseing")
    if not (new_status, new_len) == (status_code, full_len):
        prep_full.headers["user-agent"] = org_user_agent
    return  prep_full


def process(line):
    req = parse(line)
    global s
    global full_status
    global full_len
    s = Session()
    prep_full = req.prepare()
    prep_plain = copy.deepcopy(prep_full)
    prep_plain.headers = structures.CaseInsensitiveDict()

    log.debug("Probing full request")
    full_status_code, full_len = send(prep_full)
    log.debug("Probing plain request")
    plain_status_code, plain_len = send(prep_plain)

    if not full_status_code == 200:
        log.error(f"Aborting: supplied curl command not exiting with status 200: {full_status_code}")
        sys.exit()

    if plain_status_code == full_status_code and full_len == plain_len:
        log.debug("Done. All headers have no effect")
        return prep_plain

    log.debug("Some Headders appear relevant. Starting triage")
    prep_minimum = triage(prep_full, full_status_code, full_len)


    if 'user-agent' in prep_minimum.headers:
        prep_minimum = condense(prep_minimum, full_status_code, full_len)

    return prep_minimum


if __name__ == "__main__":

    # for fc + vim usecase:
    # detect if calling process is editor
    # set non verbose logging then
    if os.readlink("/proc/%s/exe" % os.getppid()).endswith(("/vi", "/vim")):
        for log_level in ["DEBUG", "INFO", "WARN"]:
            log.disable(log_level)

    for line in fileinput.input():
        log.debug(f"Processing line: {line}")
        request_obj = process(line)
        print(curlify.to_curl(request_obj))
        # try:
        #    process(line)
        # except:
        #    print("line failed: ", line)
