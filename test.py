#! /usr/bin/env python
# -*- coding: utf-8 -*-


from app.wsd.lesk import refineSentence


def test_refineSentence():
    input = "I am Robinson's son. I am 12 years old."
    output = [u'robinson', u'son', u'years', u'old']

    res = refineSentence(input)

    if(res==output):
        print "Ok......."
    else:
        print "Not Ok......"


if __name__ == "__main__":

    print "\n \t <--------------- Testing -----------------> \n"
    print "1) Testing RefineSentence"
    test_refineSentence()

    print "\nTesting Done."
