#! /usr/bin/env python
# -*- coding: utf-8 -*-

from math import fabs
from app.wsd.lesk import refineSentence, overlapScore, join_nouns, get_nouns


def test_refineSentence():
    input = "I am Robinson's son. I am 12 years old."
    output = [u'robinson', u'son', u'years', u'old']

    res = refineSentence(input)

    if(res==output):
        print "Ok......."
    else:
        print "Not Ok......"


def test_overlapScore():
    allowed_err = 1e-05
    sent1 = "There must be a tree of apple and we are in cold places."
    sent2 = "Tree of apple cultivated in cold places."
    res = overlapScore(sent1,sent2)

    if(fabs(res - 0.417321650059) <= allowed_err):
        print "Ok......."
    else:
        print "Not Ok......"


def test_join_nouns():
    nouns = { u'rocker': u'Rocker', u'celina': u'Celina', u'lincoln': u'Lincoln', u'raymond': u'Raymond' }
    para  = "Raymond is a lincoln assistant. celina lincoln is lincoln wife. Rocker Raymond is funny guy."

    res = join_nouns(nouns, para)
    output = {'Lincoln': 1.9913333333333334, 'Raymond': 1.0, 'Rocker Raymond': 0.9573333333333334, 'Celina Lincoln': 0.9786666666666667}

    if (res == output):
        print "Ok......."
    else:
        print "Not Ok......"


if __name__ == "__main__":

    print "\n \t <--------------- Testing -----------------> \n"
    print "1) Testing RefineSentence"
    test_refineSentence()
    print "\n\n2) Testing overlapScore"
    test_overlapScore()
    print "\n\n3) Testing join_nouns"
    test_join_nouns()


    print "\nTesting Done."
