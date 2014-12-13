#! /usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import numpy
import json
import re
import math
import string
import operator
import wikipedia
import traceback
import collections
from bs4 import BeautifulSoup
from urllib3 import PoolManager
from nltk.corpus import stopwords
from operator import itemgetter
from pattern.en import singularize
from nltk.tokenize import RegexpTokenizer
from string import digits
from wiki import WikiApi
from worker import qH
from worker import qL
from worker import rDB
from redis_collections import Dict

# Regex holder for noun terms
regex = re.compile("NN.*")

# Tokenizer for Punctuations
tokenizer = RegexpTokenizer(r'\w+')

functionwords = ['about', 'across', 'against', 'along', 'around', 'at',
                 'behind', 'beside', 'besides', 'by', 'despite', 'down',
                 'during', 'for', 'from', 'in', 'inside', 'into', 'near', 'of',
                 'off', 'on', 'onto', 'over', 'through', 'to', 'toward',
                 'with', 'within', 'without', 'anything', 'everything',
                 'anyone', 'everyone', 'ones', 'such', 'it', 'itself',
                 'something', 'nothing', 'someone', 'the', 'some', 'this',
                 'that', 'every', 'all', 'both', 'one', 'first', 'other',
                 'next', 'many', 'much', 'more', 'most', 'several', 'no', 'a',
                 'an', 'any', 'each', 'no', 'half', 'twice', 'two', 'second',
                 'another', 'last', 'few', 'little', 'less', 'least', 'own',
                 'and', 'but', 'after', 'when', 'as', 'because', 'if', 'what',
                 'where', 'which', 'how', 'than', 'or', 'so', 'before', 'since',
                 'while', 'although', 'though', 'who', 'whose', 'can', 'may',
                 'will', 'shall', 'could', 'be', 'do', 'have', 'might', 'would',
                 'should', 'must', 'here', 'there', 'now', 'then', 'always',
                 'never', 'sometimes', 'usually', 'often', 'therefore',
                 'however', 'besides', 'moreover', 'though', 'otherwise',
                 'else', 'instead', 'anyway', 'incidentally', 'meanwhile',
                 'article', 'articles']

# List of all Stopwords
allStopWords = set(stopwords.words('english')).union(functionwords)

def refineSentence(sentence):
    # Convert unicode to string
    sentence = sentence.encode('utf8')

    # Convert sentence to lowercase
    sentence = sentence.lower()

    # Remove digits from the sentence
    sentence = sentence.translate(None, digits)

    # Convert string to unicode
    sentence = sentence.decode('utf8')

    # Tokenize sentence into words and also removes punctuations
    words = tokenizer.tokenize(sentence)

    # Remove stopwords if exist
    words = [word for word in words if word not in allStopWords]

    return words

def intersection(text1, text2):
    score = 0

    # A counter object for holding counts of words in text2
    c = collections.Counter(text2)

    # For distinct words in text1
    for word in set(text1):
        # If this word is in text2 as well
        # then add all of its occurrences in score
        if word in text2:
            score += c[word]

    return score

def overlapScore( sentence1, sentence2 ):
    # Refine both sentences (i.e eliminate unwanted symbols,words)
    gloss1 = refineSentence(sentence1)
    gloss2 = refineSentence(sentence2)

    overlap = intersection(gloss1, gloss2)

    # Return a score using
    # https://drive.google.com/file/d/0ByirQonZ9d0HMDVycFlRX3BLa2s/view
    score = 0
    if(len(gloss2) > 0):
        score = float(math.tanh(float(overlap/(float(len(gloss1) + len(gloss2))))))
    return score


# Uses WikiPedia API to fetch articles based on input nouns
def fetch_data_from_wiki(nouns):
    print("Fetching Data from Wikipedia...")
    wiki = WikiApi()
    articles = []
    try:
        titles = []
        for noun in nouns:
            suggestions = wikipedia.search(noun)
            # Only looks for first five titles found with this word
            titles.extend(suggestions[:5])

        titles = set([ title.encode('utf-8') for title in titles])
        articles = wiki.get_articles(titles)
    except:
        print traceback.format_exc()
        print 'Error in Wikipedia Api'
    return articles


# Join nouns which occurs together and delete repeated nouns
def join_nouns(single_nouns, text):

    # Incoming list Data to dictionary
    raw_nouns_single = {}

    # Get a punctuation set
    puncset = set(string.punctuation)

    for x in single_nouns:

        t_str = single_nouns[x].capitalize()
        s = ''.join(ch for ch in t_str if ch not in puncset)
        raw_nouns_single[s] = t_str

    #print raw_nouns_single
    #print text

    # List of content, input text splitted into single word excluding these
    puncset.remove('.')
    puncset.remove(',')
    puncset.remove(';')
    puncset.remove('-')
    puncset.remove('_')
    res = "".join(c for c in text if c not in puncset)

    listofcontent =  re.findall(r"[\w']+|[.,;]",res)

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

    # Ranks nouns according to thier position in text
    for x in result:
        noun = result[x]

        # Count no. of occurences of current singular word in text
        result[x] = noun - (text.lower().find(x.lower())/float(len(text.split(' ')) * 100))

    # Result contains raw joined nouns, Passed Joined and single nouns for filter
    # joined_nouns = multiple_noun_eliminator(result)

    # return joined_nouns
    return result


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

    return joined_nouns

def get_nouns(text):

    # Remove unwanted symbols from text and tokenize it
    refined_text = refineSentence(text)

    # Dict to store nouns
    nouns = {}

    # Dict to store nouns counts
    ranks = {}

    # Tokenize input text using NLTK
    data = set(nltk.pos_tag(refined_text))

    for k,v in data:
        if regex.match(v):
            nouns[k] = k.capitalize()

    # Get joined adjacent nouns and ranks
    ranks = join_nouns(nouns, text)

    # Adds up the count of singular and plural nouns
    for k,v in ranks.items():

        token = nltk.pos_tag(nltk.tokenize.word_tokenize(k))
        print token
        if token[0][1] != "NNP":

            singular = singularize(k);

            if k != singular and ranks.has_key(singular):
                ranks[k] = ranks[k] + ranks[singular]
                del ranks[singular]

    all_nouns = sorted(ranks.items(), key=operator.itemgetter(1), reverse = True)

    print all_nouns
    print len(all_nouns)
    print len(text.split(' '))
    # No. of nouns qualified to pass to Wikipedia API
    qualifiers_count = 3 + int(math.floor(math.tanh(len(all_nouns)/float(len(text.split(' '))) * 7)))

    # If qualifiers_count exceeds total number of nouns found(highly unlikely)
    if len(all_nouns) < qualifiers_count:
        qualifiers_count = len(all_nouns)

    nouns = [ noun[0] for noun in all_nouns[:qualifiers_count] ]
    print nouns

    d = Dict(redis=rDB)
    d.update({'text' : text, 'all_nouns' : all_nouns, 'nouns' : nouns , 'status' : 'pending' })

    response = dict()
    response.update({'id' : d.key, 'all_nouns': d['all_nouns'], 'status': d['status'] })

    # Enqueue job in redis-queue
    qH.enqueue(process_job, d.key)

    return response

def process_job(job_key):
    data = Dict(key=job_key)
    data.update( { 'status' : 'started' } )

    articles = fetch_data_from_wiki(data['nouns'])
    for article in articles:
        print '\n\n Heading %s \n' % (article.heading)
        article.score = overlapScore(data['text'], article.content)
        print '\n\n'

    # Sort the articles in decreasing order of score
    articles.sort(key=lambda article: article.score, reverse=True)

    for article in articles:
        print '%s has Score = %lf' % (article.heading, article.score)

    final_articles = [ article.get_dict() for article in articles[:3] ]

    data.update({ 'status' : 'finished', 'result' : final_articles })


def get_result(job_key):
    data = Dict(key=job_key)

    result = {}
    if(data['status']=='finished'):
        result.update({ 'id' : data.key, 'status' : data['status'] , 'pages' : data['result'] })
    else:
        result.update({ 'id' : data.key, 'status' : data['status'] })

    return result

def scrape_text(url):
    #PoolManager keep the connection state
    http = PoolManager()
    r = http.request('GET', url)
    print r.status
    if r.status == 200:
        webhtml = r.data
        soup = BeautifulSoup(webhtml)

        # Just get the (meaningful) data fromparas and article tags
        text = '.'.join([str(article) for article in soup.find_all('article')])
        text = text + " " + '.'.join([str(para) for para in soup.find_all('p')])

        # Get the textual content from paras and article tags
        rawtext = BeautifulSoup(text).get_text()
        print "URL content fetched"
        return rawtext
    else:
        return "Error"
