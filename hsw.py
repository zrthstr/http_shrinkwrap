#!/usr/bin/env python3

# read curl commands form stdin
# get rid of all curl paramters that dont seem to make a difference
# write curl command back to stdout
#
# limitation: only a small subset of curl is supported,
# the parameters that come from chrome > copy_as_curl...
#
# Note:
# we shall not mess with all headder! Else 'request' will get sad/angry and die!
# e.g. Content-Length is not optional in POST requests.
# Removing such results in sadness expressed by a stack trace in requests/adapters.py

# what's next?
#  condense cookies?

import os
import sys
import copy
import uncurl
import hashlib
import curlify
import fileinput

from requests import Request, Session, structures
from loguru import logger as log


def send(seq, log_msg="headers"):
    if isinstance(seq.body, str):
        seq.body = seq.body.encode()
    resp = session.send(seq)
    log.trace(
        f"{log_msg}: {len(seq.headers)}, reply len: {len(resp.text)} status {resp.status_code}"
    )
    if not resp.status_code == 200:
        log.error(f"Supplied curl command not exiting with status 200: {resp.status_code}")
        sys.exit()

    if len(resp.text) == 0:
        log.warning("Original requests reply has length 0. Continuing")

    return resp.status_code, hashlib.sha256(resp.text.encode('utf-8')).hexdigest()


def parse(line):
    ## uncurl doesn't guarantee an url scheme while curlify insists on having one
    context = uncurl.parse_context(line)

    if not context.url.startswith("http"):
        context = context._replace(url="http://" + context.url)
    req = Request(
        context.method.upper(), context.url, headers=context.headers, data=context.data
    )
    return req


def is_same_without(prep, without, full_status_code, full_hash):
    one_less = copy.deepcopy(prep)
    del one_less.headers[without]

    new_status, new_hash = send(one_less)
    if new_status == full_status_code and new_hash == full_hash:
        return False
    return True


def triage(prep_full, full_status_code, full_hash):
    log.debug("Some Headders appear relevant. Starting triage")
    header_count = len(prep_full.headers)
    if len(prep_full.headers) == 1:
        return prep_full

    log.debug(f"Starting triage with: {header_count} headers")

    obsolete_headers = structures.CaseInsensitiveDict()
    needed_headers = structures.CaseInsensitiveDict()
    for headder_name, headder_value in prep_full.headers.items():
        #print("x" * 20, headder_name)
        if headder_name == "Content-Length":
            needed_headers[headder_name] = headder_value
            continue

        if is_same_without(prep_full, headder_name, full_status_code, full_hash):
            log.debug(f"Found needed headder: {headder_name, headder_value}")
            needed_headers[headder_name] = headder_value
        else:
            log.debug(f"Found obsolete headder: {headder_name, headder_value}")
            obsolete_headers[headder_name] = headder_value
            # del header

    prep_full.headers = needed_headers
    return prep_full


def condense(prep_full, full_status_code, full_hash):
    """ try to shorten User-Agent"""
    if not 'User-Agent' in prep_full.headers:
        return prep_full

    max_user_agent_len = 15
    org_user_agent = prep_full.headers["User-Agent"]
    log.debug(f'condensing User-Agent: {org_user_agent}')
    if " " in org_user_agent.lower():
        prep_full.headers["User-Agent"] = org_user_agent.split()[0]
    elif len(org_user_agent) > max_user_agent_len:
        prep_full.headers["User-Agent"] = org_user_agent[0:max_user_agent_len]
    else:
        # no change, no test needed
        return prep_full

    # make sure condensing has no side effect
    new_status, new_hash = send(prep_full, log_msg="condenseing")

    if (new_status, new_hash) != (full_status_code, full_hash):
        prep_full.headers["User-Agent"] = org_user_agent
    return  prep_full


def check_flapping(full_status_code, full_hash, prep_full ):
    check_status_code, check_hash = send(prep_full)
    if full_status_code == check_status_code and full_hash == check_hash:
        log.debug("No flapping detected")
    else:
        log.error("Aborting. Two response to the same queries diverge")
        sys.exit(3)


def ensure_post_content_length_header(prep_plain):
    # needed to ensure requests fills in correct value
    if prep_plain.method == "POST":
        prep_plain.headers['Content-Length'] = 0
    return prep_plain


def prepare_plain_request(prep_full):
    prep_plain = copy.deepcopy(prep_full)
    prep_plain.headers = structures.CaseInsensitiveDict()
    return ensure_post_content_length_header(prep_plain)



def get_full_and_plain(prep_full, prep_plain):
    log.debug("Probing two full requests")
    full_status_code, full_hash = send(prep_full)
    plain_status_code, plain_hash = send(prep_plain)
    return full_status_code, full_hash, plain_status_code, plain_hash


def process(line):
    global session
    session = Session()
    req = parse(line)

    prep_full = session.prepare_request(req)
    prep_plain = prepare_plain_request(prep_full)
    full_status_code, full_hash, plain_status_code, plain_hash = get_full_and_plain(prep_full, prep_plain)

    check_flapping(full_status_code, full_hash, prep_full)

    if plain_status_code == full_status_code and full_hash == plain_hash:
        log.debug("Done. All headers have no effect")
        return prep_plain

    prep_minimum = triage(prep_full, full_status_code, full_hash)
    prep_minimum = condense(prep_minimum, full_status_code, full_hash)

    return prep_minimum


def handle_editor():
    """
    adjust log level for  fc + vim usecase:
    if calling process is editor, set non verbose logging
    """
    log.remove()
    if os.readlink("/proc/%s/exe" % os.getppid()).endswith(("/vi", "/vim")):
        log.add(sys.stderr, level="ERROR")
    else:
        log.add(sys.stderr, level="DEBUG")


if __name__ == "__main__":
    handle_editor()
    for curl_line in fileinput.input():
        log.debug(f"Processing curl: {curl_line}")
        request_obj = process(curl_line)

        print(curlify.to_curl(request_obj))

