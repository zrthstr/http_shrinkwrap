#!/usr/bin/env python3

from random import randint


from flask import Flask, request
app = Flask(__name__, static_folder=None)

@app.route('/')
def info_rsq():
    #print(app.url_map)
    return f'{str(app.url_map)}\n\n{str(request.headers)}\n'

@app.route('/empty')
def empty_req():
    return ''

@app.route('/static')
def vanilla_rsq():
    return 'Static\n'

@app.route('/random')
def random_rsq():
    return str(randint(1E4,int(1E16))) + '\n'

### some headers needed
@app.route('/some', methods=['GET', 'POST'])
def some_headers_need_rsq():
    if 'Needed-0' in request.headers and 'Needed-1' in request.headers:
        if request.headers['Needed-0'] == 'Is-0' and request.headers['Needed-1'] == 'Is-1':
            return 'OKEY'
    return 'NOPE'

## long user agent. only first N chars matters
@app.route('/useragent')
def user_agent_req():
    if 'User-Agent' in request.headers:
        if request.headers['User-Agent'].startswith('Mozilla'):
            return 'OKEY'
    return 'NOPE'

@app.route('/null', methods=['GET', 'POST'])
def null_req():
    if 'Needed-0' in request.headers:
        if request.headers['Needed-0'] == 'Is-0':
            return ''
    return 'NOPE'

@app.route('/post', methods=['POST'])
def post_req():
    print('headers:', request.headers)
    print('data:', request.data)
    print('args:', request.args)
    print('form:', request.form)
    print('files:', request.files)
    print('values:', request.values)
    return 'OKEY'

@app.route('/post_some', methods=['POST'])
def post_some():
    if 'Needed-0' in request.headers:
        if request.headers['Needed-0'] == 'Is-0':
            return 'OKEY'
    return 'NOPE'


@app.route('/get_304')
def get_304():
    ''' if cache headers present, reply with 304'''
    headers = ['if-Modified-Since', 'If-Unmodified-since', 'If-Match', 'If-None-Match']
    if not 'Needed-0' in request.headers:
        return 'BAD'

    for h in headers:
        if h in request.headers:
            return "", 304
    return 'just your average joe non cached response'


if __name__ == '__main__':
    app.run(port=8000)
