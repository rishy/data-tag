import nltk
import numpy
import json
import re
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
from flask.ext.cors import cross_origin

# can be removed once installed
nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')

@app.route('/')
def root():
    return app.send_static_file('index.html')

def is_contain(payload,*args):
    for a in args:
        if not a in payload:
            return False
    return True

@app.route('/api/tagit/v1.0/', methods= ['OPTIONS','POST'])
@cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
def apiTagit():
    if request.method == 'OPTIONS':
        return make_response(jsonify({"Allow":"POST"}),200)

    if not request.json or not is_contain(request.json,'text'):
        abort(400)
    # Json data extraction
    text = request.json['text']

    # Tokenize input text using NLTK
    data = nltk.pos_tag(nltk.tokenize.word_tokenize(text))
    print data

    # Json Object to store nouns
    nouns = {}

    # Regex holder for noun terms
    a = re.compile("NN.*")

    for word in data:
        if a.match(word[1]):
            nouns[word[0]] = word[0];

    # leave this intact, will be used for further robustness
    '''data_len = len(data)
    i = 0

    while i < data_len:
        temp_list = []
        if nouns.__contains__(data[i]):
            temp_list.append(data[i]);
            while ++i < data_len:
                if nouns.__contains__(data[i]):
                    temp_list.append(data[i]);

        for word in temp_list:
            nouns.pop(word)

        str = " ".join(temp_list)
        nouns[str] = str'''

    json_data = json.dumps(nouns)
    print json_data
    return make_response(json_data,200)


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

