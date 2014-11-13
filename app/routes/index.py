import nltk
import numpy
import json
import re
import wikipedia
import operator
from nltk.corpus import stopwords
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
from operator import itemgetter
from pattern.en import singularize

# can be removed once installed
#nltk.download('punkt')
#nltk.download('maxent_treebank_pos_tagger')
nltk.download('stopwords')

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
    print("Fetching Data from Wikipedia...")
    tags = []
    for noun in nouns:
        pages = []
        pages = wikipedia.search(noun[0])
        for page in pages:
            wiki_content = wikipedia.page(page).summary
            tags.append(wiki_content)
            #tags.append(run_wsd(wiki_content, in_text))
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
    
    # Futile stopwords
    sw = stopwords.words('english')
    
    # Json Objects to store nouns
    nouns = {}

    # List to store nouns counts
    nouns_counts = {}
    
    # Regex holder for noun terms
    a = re.compile("NN.*")

    # Json data extraction
    text = request.json['text']

    # Tokenize input text using NLTK
    data = set(nltk.pos_tag(nltk.tokenize.word_tokenize(text.lower())))
    #print (data)   

    for word in data:

        w = realW = word[0]

        # Singularizing proper, singular, nouns(NNP) may result in errors
        if word[1] != "NNP":
            w = singularize(w)

        if a.match(word[1]) and realW not in nouns.keys() and w not in sw:

            nouns[w] = w.capitalize()

            # Tokenize all the words in input text
            token = nltk.tokenize.word_tokenize(text.lower())

            # Count no. of occurences of current singular word in text
            nouns_counts[w] = token.count(w)

            # If word has been singularized, also count its original plural form
            if w != realW:                
                nouns_counts[w] += token.count(realW)

    # Gets the sorted nouns_counts according to the no. of occurrences
    nouns_counts = sorted(nouns_counts.items(), key=operator.itemgetter(1), reverse = True)

    # Nouns to be passed to wikipedia API
    top_nouns = nouns_counts[:]
    print top_nouns
    # print nouns
   
    # Use Wikipedia API to get content based on found nouns and then run WSD
    '''tags = get_wiki_data(top_nouns, text)
    print tags[0]
    print("-----------------------------------------------")
    print tags[1]'''
    '''jsonify this "tags" list as the final output'''
   

    json_data = json.dumps(nouns)
    # print json_data
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

