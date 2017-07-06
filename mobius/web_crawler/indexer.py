# -*- coding: utf-8 -*-
import random
import nltk


class Indexer(object):

    def __init__(self, index):
        self._index = index

    def process_page(self, url, tree):
        """
        Indexes a given page.

        :param url:  URL for web page.
        :param tree: Tree representing parse web page.
        """
        # Get title
        xpath = '/html/head/title/text()'
        title = tree.xpath(xpath)
        if title is None or len(title) != 1:
            # Ignore pages without a title
            return
        title = title.pop().strip()  # Remove whitespace at beginning/end

        xpath = "/html/head/meta[@name='description']/@content"
        description = tree.xpath(xpath)
        if description is None or len(description) != 1:
            # Ignore pages without a description
            return
        description = description.pop()

        # Parse description
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(description))
        weighted_keywords = []
        for token, tag in tagged_tokens:
            if tag in ['NN', 'NNP']:  # If noun or proper noun
                weighted_keywords.append((token, random.randint(0, 100)))

        self._index.index_site(url, weighted_keywords)
