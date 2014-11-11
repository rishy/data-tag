import nltk
import numpy
import json
import re
import wikipedia
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
#nltk.download('punkt')
#nltk.download('maxent_treebank_pos_tagger')

@app.route('/')
def root():
    return app.send_static_file('index.html')

def is_contain(payload,*args):
    for a in args:
        if not a in payload:
            return False
    return True

# Uses WikiPedia API to fetch pages based on input nouns 
def get_wiki_data(nouns, in_text):
    # A list to store final tags output
    tags = []
    for noun in nouns_list:
        pages = []
        pages = wikipedia.search(noun)
        for page in pages:
            wiki_content = wikipedia.page(page).content
            tags.append(run_wsd(wiki_content, in_text))
    return tags

# Runs Word-Sense Disambiguation Algorithm to fetch the approporiate tag
def run_wsd(content, text):
    # A JSON object to store tag data
    tag_data = {}

    '''
        Code for Word-Sense Disambiguation Algorithm to filter out the 
        possible-tag data.
    '''

    return tag_data

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

    # List to store nouns
    nouns_list = []

    # Regex holder for noun terms
    a = re.compile("NN.*")

    # Create the response JSON Object for found nouns
    for word in data:
        if a.match(word[1]):
            nouns[word[0]] = word[0];
            nouns_list.append(word[0]);

    '''
    # Use Wikipedia API to get content based on found nouns and then run WSD
    tags = get_wiki_data(nouns_list, text)

        jsonify this "tags" list as the final output
    '''

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

