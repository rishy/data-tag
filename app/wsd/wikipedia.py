#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the wikipedia api wrapper derived from
repository on github.

Repo Link:-  https://github.com/richardasaurus/wiki-api

In this some additional functionality added like to get
the content of multiple wikipedia pages.

"""
from xml.dom import minidom
from pyquery import PyQuery
import requests
import grequests
import urllib
import re

uri_scheme = 'http'
api_uri = 'wikipedia.org/w/api.php'
article_uri = 'wikipedia.org/wiki/'

#common sub sections to exclude from output
unwanted_sections = [
    'External links',
    'Navigation menu',
    'See also',
    'References',
    'Further reading',
    'Contents',
    'Official',
    'Other',
    'Notes',
]


class WikiApi:

    def __init__(self, options=None):
        if options is None:
            options = {}

        self.options = options
        if 'locale' not in options:
            self.options['locale'] = 'en'

    def find(self, terms):
        search_params = {'action': 'opensearch',
                         'search': terms,
                         'format': 'xml'}
        url = self.build_url(search_params)
        resp = self.get(url)

        #parse search results
        xmldoc = minidom.parseString(resp)
        items = xmldoc.getElementsByTagName('Item')

        #return results as wiki page titles
        results = []
        for item in items:
            link = item.getElementsByTagName('Url')[0].firstChild.data
            slug = re.findall(r'wiki/(.+)', link, re.IGNORECASE)
            results.append(slug[0])
        return results

    def get_article(self, title):
        """
        Fetch the content and other relevant information of single wikipedia page.
        """
        url = self.form_article_url(title)
        article = self.clean_html(self.get(url), url)
        return article

    # Additionally added feature
    def get_articles(self, titles):
        """
        Fetch the content and other relevant information of multiples wikipedia page.
        """
        # Create a list of urls from titles
        urls = []
        for title in titles:
            url = self.form_article_url(title)
            urls.append(url)
        print urls
        # Create a set of unsent Requests
        rs = (grequests.get(u) for u in urls)

        # Send them all at the same time
        res = grequests.map(rs, stream=False)

        # Extact article content from html
        articles = []
        for url, r in zip(urls, res):
            article = self.clean_html(r.text, url)
            articles.append(article)
        return articles

    def get_relevant_article(self, results, keywords):
        """
        Get the most relevant article from the results of find(),
        using a list of keywords and checking for them in article.summary
        """
        for result in results:
            article = self.get_article(result)
            summary_words = article.summary.split(' ')
            has_words = any(word in summary_words for word in keywords)
            if has_words:
                return article
        return None

    def build_url(self, params):
        default_params = {'format': 'xml'}
        query_params = dict(
            list(default_params.items()) + list(params.items()))
        query_params = urllib.urlencode(query_params)
        return '{0}://{1}.{2}?{3}'.format(
            uri_scheme, self.options['locale'], api_uri, query_params)

    def get(self, url):
        r = requests.get(url)
        return r.content

    # form an article url of wikipedia
    def form_article_url(self, title):
        url = '{0}://{1}.{2}{3}'.format(uri_scheme, self.options['locale'], article_uri, title)
        return url

    # clean the html content and return Article class object
    def clean_html(self, content, url):
        html = PyQuery(content)
        data = dict()

        # parse wiki data
        data['heading'] = html('#firstHeading').text()
        paras = html('.mw-content-ltr').find('p')
        data['image'] = 'http:{0}'.format(html('body').find('.image img').attr('src'))
        data['summary'] = str()
        data['full'] = unicode()
        references = html('body').find('.web')
        data['url'] = url

        # gather references
        data['references'] = []
        for ref in references.items():
            data['references'].append(self.strip_text(ref.text()))

        # gather summary
        summary_max = 900
        chars = 0
        for p in paras.items():
            if chars < summary_max:
                chars += len(p.text())
                data['summary'] += '\n\n' + self.strip_text(p.text())

        # gather full content
        for idx, line in enumerate(html('body').find('h2, p').items()):
            if idx == 0:
                data['full'] += data['heading']

            clean_text = self.strip_text(line.text())
            if clean_text:
                data['full'] += '\n\n' + clean_text

        data['full'] = data['full'].strip()
        article = Article(data)
        return article

    # remove unwanted information
    def strip_text(self, string):
        #remove citation numbers
        string = re.sub(r'\[\s\d+\s\]', '', string)
        #remove wiki text bold markup tags
        string = re.sub(r'"', '', string)
        #correct spacing around fullstops + commas
        string = re.sub(r' +[.] +', '. ', string)
        string = re.sub(r' +[,] +', ', ', string)
        #remove sub heading edits tags
        string = re.sub(r'\s*\[\s*edit\s*\]\s*', '\n', string)
        #remove unwanted areas
        string = re.sub("|".join(unwanted_sections), '', string, re.IGNORECASE)
        return string


class Article:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.heading = data.get('heading')
        self.image = data.get('image')
        self.summary = data.get('summary')
        self.content = data.get('full')
        self.references = data.get('references')
        self.url = data.get('url')
        self.score = 0.0

    def __repr__(self):
        return '<wikiapi.Article {0}>'.format(self.heading)

    def get_dict(self):
        res = {}
        res['heading'] = self.heading
        res['image'] = self.image
        res['summary'] = self.summary
        res['content'] = self.content
        res['references'] = self.references
        res['url'] = self.url
        res['score'] = self.score
        return res

    def print_article(self):
        print 'Heading => %s ' % (self.heading)
        print 'Url     => %s ' % (self.url)
        print 'Summary: \n%s ' % (self.summary[:100].strip())
        print 'Content: \n%s ' % (self.content[:100].strip())
        print '\n\n'
