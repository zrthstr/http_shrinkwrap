#!/usr/bin/env python3

#import os
#import sys
#import copy
#import uncurl
#import hashlib
import curlify
import fileinput

from .api import * # this is ugly!

#from requests import Request, Session, structures
#from loguru import logger as log



if __name__ == "__main__":
    config_logging()

    if is_called_from_vim():
        curl_line = vim_line_merge()
    else:
        curl_line = fileinput.input()[0]

    log.debug(f"Processing curl: {curl_line}")
    request_obj = process(curl_line)
    print(curlify.to_curl(request_obj))

