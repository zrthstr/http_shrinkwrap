#!/usr/bin/env python3

# read curl commands form stdin
# get rid of all curl paramters that dont seem to make a difference
# write curl command back to stdout
#
# limitation: only a small subset of curl is supported,
# the parameters that come from chrome > copy_as_curl...
#
# Note:
# we shall not mess with all headder! For else 'request' will get sad/angry and die!
# e.g. Content-Length headder is not optional in POST requests.
# Removing such would result in sadness, expressed by a stack trace in requests/adapters.py

import os
import sys
import copy
import psutil
import hashlib
import fileinput

import uncurl

from requests import Request, Session, structures
from loguru import logger as log

#global SESSION

def send(seq, log_msg="headers"):
    if isinstance(seq.body, str):
        seq.body = seq.body.encode()
    resp = SESSION.send(seq)
    log.trace(
        f"{log_msg}: {len(seq.headers)}, reply len: {len(resp.text)} status {resp.status_code}"
    )
    if resp.status_code == 304:
        log.error(f"Supplied curl command returned 304.\n"
                " Consider using the --bust flag to remove the headers that mightbe causing this.")
        sys.exit(48) # 304 % 256
    elif not resp.status_code == 200:
        log.error(f"Supplied curl command did not return status 200: {resp.status_code}")
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

    # make sure, condensing has no side effect
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
    # needed to ensure requests fills in the correct value
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

def remove_cache_header(req):
    log.trace("Looking for cache headers to remove")
    for header in req.headers:
        if header.lower() in ["if-modified-since", "if-none-match", "if-match", "if-unmodified-since"]:
            log.debug(f"Removing cache header: {req.headers[header]}")
            del(req.headers[header])
    return req

def process(line, rm_cache_header):
    global SESSION
    SESSION = Session()
    req = parse(line)

    prep_full = SESSION.prepare_request(req)

    if rm_cache_header:
        prep_full = remove_cache_header(prep_full)

    prep_plain = prepare_plain_request(prep_full)

    full_status_code, full_hash, plain_status_code, plain_hash = \
            get_full_and_plain(prep_full, prep_plain)

    check_flapping(full_status_code, full_hash, prep_full)

    if plain_status_code == full_status_code and full_hash == plain_hash:
        log.debug("Done. All headers have no effect")
        return prep_plain

    prep_minimum = triage(prep_full, full_status_code, full_hash)
    prep_minimum = condense(prep_minimum, full_status_code, full_hash)

    return prep_minimum


def config_logging():
    """
    if calling process is editor, or env DEBUG=TRUE set non verbose logging
    """
    log.remove()
    if os.environ.get('DEBUG') == "TRUE":
        log.add(sys.stderr, level="DEBUG")
    elif os.environ.get('DEBUG') == "TRACE":
        log.add(sys.stderr, level="TRACE")
    elif is_called_from_vim():
        log.add(sys.stderr, level="ERROR")
    else:
        log.add(sys.stderr, level="WARNING")


def is_called_from_vim():
    try:
        if psutil.Process(os.getppid()).name() in ["vim","vi"]:
            return True
    except:
        return False


def vim_line_merge():
    last = ""
    for curl_line in fileinput.input():
        if curl_line[-2:] == '\\\n':
            last = last + curl_line[:-2]
            continue
    return last
