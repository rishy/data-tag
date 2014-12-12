#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from flask import make_response
from flask import jsonify
from flask.ext.cors import CORS, cross_origin
from app.wsd import get_result
import json

def is_contain(payload,*args):
    for a in args:
        if not a in payload:
            return False
    return True

# Routing for homepage/root page
@app.route('/')
def root():
    return app.send_static_file('index.html')


# Routing for tagit api
@app.route('/api/tagit/v1.0/', methods= ['OPTIONS','POST'])
@cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
def apiTagit():
    print 'I got an api request'
    print 'Method Type: %s' % request.method
    print 'Content : %s' % request.json
    print request.headers
    if request.method == 'OPTIONS':
        return make_response(jsonify({"Allow":"POST"}),200)

    if not request.json or not is_contain(request.json,'text'):
        print 'Bad Request'
        abort(400)

    # Get the text from json request data
    text = request.json['text']

    # Get the result
    result = get_nouns(text)

    result = json.dumps(result)

    return make_response(result,200)

# Routing for tagit api
@app.route('/api/tagit/v1.0/result/', methods= ['OPTIONS','POST'])
@cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
def apiTagit():
    print 'I got an api request'
    print 'Method Type: %s' % request.method
    print 'Content : %s' % request.json
    print request.headers
    if request.method == 'OPTIONS':
        return make_response(jsonify({"Allow":"POST"}),200)

    if not request.json or not is_contain(request.json,'id'):
        print 'Bad Request'
        abort(400)

    # Get the job-key from json request data
    key = request.json['id']

    # Get the result
    result = get_result(text)

    result = json.dumps(result)

    return make_response(result,200)


# app error handler
@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

