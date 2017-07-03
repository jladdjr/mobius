# !/usr/bin/env python

from mobius.web_crawler import parser, indexer
from mobius.utils import cleanURLs

"""
Simple web crawler.
"""

import random


class WebCrawler(object):
    """
    Web Crawler.
    """

    def __init__(self, startURL="http://en.wikipedia.org"):
        """
        Initializes WebCrawler object.

        :param startURL: First page web crawler visits.
        """
        self._startURL = startURL       # First page to index
        self._indexer = indexer.Indexer()

    def run(self, numPages):
        """
        Starts web crawler.

        :param numPages: Number of pages web crawler visits.
        """
        print("Indexing..")
        print("")

        # Begin with starting page
        url = self._startURL

        # Keep track of previous url. Will return to this
        # if a page is unavailable (or unreadable)
        previousURL = url

        # Loop to index each page
        index = 0
        while index < numPages:
            print("{0}: {1}".format(index, url))

            tree = parser.getParsedPage(url)
            if tree is None:
                url = previousURL
                tree = parser.getParsedPage(url)

            self._indexer.processPage(url, tree)

            previousURL = url
            url = self._nextPage(url, tree)
            index += 1

        print("")
        print("-----------------------------------")
        print("")
        print("Results:")
        print("")

        # Print index
        self._indexer.printIndex()

    def _nextPage(self, currentURL, tree):
        """
        Retrieves next page to process.

        If given page does not contain any URLs, returns
        the starting URL.

        :param currentURL: Current url (including protocol)
        :param tree:       Tree representing parse web page.
        :returns:          Randomly selected URL.
        """
        # Get all urls on page
        urls = tree.xpath('//@href')

        # If this page does not have any urls, return to starting page
        # TODO: Return to previous page instead of going to starting page.
        if len(urls) == 0:
            return self._startURL

        # Clean list of urls
        urls = cleanURLs(currentURL, urls)

        # Verify list of urls isn't empty
        if len(urls) == 0:
            return self._startURL

        # Pick random URL
        url = random.choice(urls)

        return url
