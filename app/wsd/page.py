#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wikipedia import WikipediaPage

class Page(object):
    def __init__(self, wiki_page):
        self.title = wiki_page.title
        self.url = wiki_page.url
        self.content = wiki_page.content
        self.summary = wiki_page.summary
        self.images = wiki_page.images
        self.links = wiki_page.links
        self.categories = wiki_page.categories
        self.score = 0

    def get_dict(self):
        res = {}
        res['title'] = self.title
        res['url'] = self.url
        res['content'] = self.content
        res['summary'] = self.summary
        res['categories'] = self.categories
        res['images'] = self.images
        res['links'] = self.links

        return res
