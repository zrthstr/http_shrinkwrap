#!/usr/bin/env python3

from random import random


from flask import Flask, request
app = Flask(__name__, static_folder=None)


#@app.route('/', methods=['GET'])

@app.route('/')
def info_rsq():
    #print(app.url_map)
    return f"{str(app.url_map)}\n\n{str(request.headers)}\n"

@app.route('/empty')
def empty_req():
    return ""

@app.route('/vanilla')
def vanilla_rsq():
    return "Vanilla\n"

@app.route('/random')
def random_rsq():
    return str(random.randint(1E4,int(1E16))) + "\n"

### some headers needed
@app.route('/some')
def some_headers_need_rsq():
    if 'Needed-0' in request.headers and 'Needed-1' in request.headers:
        if request.headers['Needed-0'] == 'Is-0' and request.headers['Needed-1'] == 'Is-1':
            return "OKEY"
    return "NOPE"

## long user agent. only first N chars matters
@app.route('/useragent')
def user_agent_req():
    if 'User-Agent' in request.headers:
        if request.headers['User-Agent'].startswith("Mozilla"):
            return "OKEY"
    return "NOPE"


if __name__ == '__main__':
    app.run(port=8000)
