import nltk
import numpy
import json
import re
import string
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
from flask.ext.cors import CORS, cross_origin
from operator import itemgetter
from pattern.en import singularize

# can be removed once installed
#nltk.download('punkt')
#nltk.download('maxent_treebank_pos_tagger')
#nltk.download('stopwords')

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


# Join nouns which occurs together and delete repeated nouns
def noun_precisor(single_nouns, text):

    # Incoming list Data to dictionary
    raw_nouns_single = {}

    puncset = set(string.punctuation)

    for x in single_nouns:
        t_str = x[0].capitalize()
        s = ''.join(ch for ch in t_str if ch not in puncset)
        raw_nouns_single[s] = x[1]
    #print raw_nouns_single
    #print text

    # List of content, input text splitted into single word excluding (.)
    puncset.remove('.')
    puncset.remove(',')
    puncset.remove(';')
    res = "".join(c for c in text if c not in puncset)
    listofcontent =  re.findall(r"[\w']+|[.,;]",res)

    #print listofcontent

    temp_nouns = []
    result = {}

    for key,val in raw_nouns_single.iteritems():
        temp_nouns.append(key)

    # To check noun counts and Joined noun text
    cnt_noun = 0
    join_noun = ""
    for i,x in enumerate(listofcontent):
        #print i,"-",x
        x = x.capitalize()
        if(x in temp_nouns):
            cnt_noun += 1
            if(join_noun == ""):
                join_noun += x
            else:
                join_noun += " " + x
            #print cnt,tmp
        else:
            if(join_noun in result.keys()):
                result[join_noun] += 1;
            else:
                result[join_noun] = 1

            join_noun = ""
            cnt_noun = 0

    blank_key = ""
    if(blank_key in result.keys()):
        del result[blank_key]

    print "---Raw Joined_Nouns(Contain multiple joined nouns)------"
    #print result
    for x,v in result.iteritems():
        print x, " - ", v


    # Result contains raw joined nouns, Passed Joined and single nouns for filter
    Nouns_wiki = multiple_noun_eliminator(result)

    return Nouns_wiki


def multiple_noun_eliminator(joined_nouns):

    tlist = []
    #temp_jnd_nouns = joined_nouns

    #print joined_nouns

    tmp_joined_nouns = []
    repeat_joined_nouns = []

    # Copy of Joined Nouns data to make list for easy operation
    for x,v in joined_nouns.iteritems():
        tmp_joined_nouns.append(x)

    backup_nouns = tmp_joined_nouns

    #All nouns matched entity removed from Joined nouns list and Occurences are merged.
    for i in range(0,len(tmp_joined_nouns)):
        text1 = tmp_joined_nouns[i].split()
        for j in range(i+1,len(backup_nouns)):
            flag = 1
            text2 = backup_nouns[j].split()
            if(len(text1) >= len(text2)):
                for x in text2:
                    if(x not in text1):
                        flag = 0
                        break
                if(flag):
                    repeat_joined_nouns.append(backup_nouns[j])
                    joined_nouns[tmp_joined_nouns[i]] += joined_nouns[backup_nouns[j]]
            else:
                for x in text1:
                    if(x not in text2):
                        flag = 0
                        break
                if(flag):
                    repeat_joined_nouns.append(tmp_joined_nouns[i])
                    joined_nouns[backup_nouns[j]] += joined_nouns[tmp_joined_nouns[i]]

    #Delete repeat_joined_nouns
    for x in repeat_joined_nouns:
        joined_nouns.pop(x, None)
    '''
    print "--------------Final Joined Nouns--------------------"
    print joined_nouns
    for x,v in joined_nouns.iteritems():
        print x, " - ", v
    print "--------------End of nouns Processing--------------------"
    '''
    return joined_nouns


# Runs Word-Sense Disambiguation Algorithm to fetch the approporiate tag
def run_wsd(content, text):
    # A JSON object to store tag data
    tag_data = {}

    '''
        Code for Word-Sense Disambiguation Algorithm to filter out the
        possible-tag data.
    '''

    return tag_data

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

    #print data

    for word in data:

        w = word[0]

        # Singularizing proper, singular, nouns(NNP) may result in errors
        '''if word[1] != "NNP":
            w = singularize(w)
        '''
        if a.match(word[1]) and w not in nouns.keys() and w not in sw:

            nouns[w] = w.capitalize()

            # Tokenize all the words in input text
            token = nltk.tokenize.word_tokenize(text.lower())

            # Count no. of occurences of current singular word in text
            nouns_counts[w] = token.count(w)

            # If word has been singularized, also count its original plural form
            if w != w:
                nouns_counts[w] += token.count(w)

    # Gets the sorted nouns_counts according to the no. of occurrences
    nouns_counts = sorted(nouns_counts.items(), key=operator.itemgetter(1), reverse = True)

    # Nouns to be passed to wikipedia API
    top_nouns = nouns_counts[:]
    #print top_nouns
    # print nouns

    # Get precise nouns (join nouns which occur together)
    Nouns_wiki = noun_precisor(top_nouns, text)

    # Adds up the count of singular and plural nouns
    for k,v in Nouns_wiki.items():

        token = nltk.pos_tag(nltk.tokenize.word_tokenize(k))
        print token
        if token[0][1] != "NNP":

            singular = singularize(k);

            if k != singular and Nouns_wiki.has_key(singular):

                Nouns_wiki[k] = Nouns_wiki[k] + Nouns_wiki[singular];
                del Nouns_wiki[singular];

    print "--------------Final Joined Nouns--------------------"

    #print Nouns_wiki, type(Nouns_wiki)
    '''
    for k,v in Nouns_wiki.iteritems():
        print k,'->',v
    '''

    # Use Wikipedia API to get content based on found nouns and then run WSD
    '''tags = get_wiki_data(top_nouns, text)
    print tags[0]
    print("-----------------------------------------------")
    print tags[1]'''
    '''jsonify this "tags" list as the final output'''

    json_data = json.dumps(Nouns_wiki)
    print sorted(Nouns_wiki.items(), key=operator.itemgetter(1), reverse = True)
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

