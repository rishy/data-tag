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
from nltk.corpus import stopwords
from operator import itemgetter
from pattern.en import singularize
from nltk.tokenize import RegexpTokenizer
from string import digits
from wiki import WikiApi

# List of English Stopwords
allStopWords = stopwords.words('english')

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
                 'else', 'instead', 'anyway', 'incidentally', 'meanwhile']

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
    words1 = refineSentence(sentence1)
    words2 = refineSentence(sentence2)

    gloss1 = [word for word in words1 if word not in functionwords]
    gloss2 = [word for word in words2 if word not in functionwords]

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
            titles.extend(suggestions[:5])

        titles = [ title.encode('utf-8') for title in titles]
        articles = wiki.get_articles(titles[:])
    except:
        print traceback.format_exc()
        print 'Error in Wikipedia Api'
    return articles


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
    # Nouns_wiki = multiple_noun_eliminator(result)

    # return Nouns_wiki
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

def get_result(text):
    # Dict to store nouns
    nouns = {}

    # Dict to store nouns counts
    nouns_counts = {}

    # Tokenize input text using NLTK
    data = set(nltk.pos_tag(nltk.tokenize.word_tokenize(text.lower())))

    for word in data:

        w = word[0]

        # Singularizing proper, singular, nouns(NNP) may result in errors
        if regex.match(word[1]) and w not in nouns.keys() and w not in allStopWords:

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

    # Get precise nouns (join nouns which occur together)
    Nouns_wiki = noun_precisor(top_nouns, text)

    # Adds up the count of singular and plural nouns
    for k,v in Nouns_wiki.items():

        token = nltk.pos_tag(nltk.tokenize.word_tokenize(k))
        print token
        if token[0][1] != "NNP":

            singular = singularize(k);

            if k != singular and Nouns_wiki.has_key(singular):
                Nouns_wiki[k] = Nouns_wiki[k] + Nouns_wiki[singular]
                del Nouns_wiki[singular]

    all_nouns = sorted(Nouns_wiki.items(), key=operator.itemgetter(1), reverse = True)

    nouns = [ noun[0] for noun in all_nouns[:3] ]
    print nouns

    articles = fetch_data_from_wiki(nouns)
    for article in articles:
        print '\n\n Heading %s \n' % (article.heading)
        article.score = overlapScore(text, article.content)
        print '\n\n'

    # Sort the articles in decreasing order of score
    articles.sort(key=lambda article: article.score, reverse=True)

    for article in articles:
        print '%s has Score = %lf' % (article.heading, article.score)

    final_articles = [ article.get_dict() for article in articles[:3] ]

    return final_articles
