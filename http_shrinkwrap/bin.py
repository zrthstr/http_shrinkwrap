#!/usr/bin/env python3

import sys
import fileinput
import curlify

#from api import config_logging, is_called_from_vim, vim_line_merge, process, log
from .api import config_logging, is_called_from_vim, vim_line_merge, process, log

def main():
    config_logging()

    if len(sys.argv) > 1 or is_called_from_vim():
        curl_line = vim_line_merge()
    else:
        curl_line = fileinput.input().__next__()

    log.debug(f"Processing curl: {curl_line}")
    request_obj = process(curl_line)
    print(curlify.to_curl(request_obj))


if __name__ == "__main__":
    main()
