# !/usr/bin/env python

from mobius.web_crawler import parser, indexer
from mobius.utils import clean_urls

"""
Simple web crawler.
"""

import random


class WebCrawler(object):
    """
    Web Crawler.
    """

    def __init__(self, start_url="http://en.wikipedia.org"):
        """
        Initializes WebCrawler object.

        :param start_url: First page web crawler visits.
        """
        self._start_url = start_url       # First page to index
        self._indexer = indexer.Indexer()

    def run(self, num_pages):
        """
        Starts web crawler.

        :param num_pages: Number of pages web crawler visits.
        """
        print("Indexing..")
        print("")

        # Begin with starting page
        url = self._start_url

        # Keep track of previous url. Will return to this
        # if a page is unavailable (or unreadable)
        previous_url = url

        # Loop to index each page
        index = 0
        while index < num_pages:
            print("{0}: {1}".format(index, url))

            tree = parser.get_parsed_page(url)
            if tree is None:
                url = previous_url
                tree = parser.get_parsed_page(url)

            self._indexer.process_page(url, tree)

            previous_url = url
            url = self._nextPage(url, tree)
            index += 1

        print("")
        print("-----------------------------------")
        print("")
        print("Results:")
        print("")

        # Print index
        self._indexer.print_index()

    def _nextPage(self, current_url, tree):
        """
        Retrieves next page to process.

        If given page does not contain any URLs, returns
        the starting URL.

        :param current_url: Current url (including protocol)
        :param tree:        Tree representing parse web page.
        :returns:           Randomly selected URL.
        """
        # Get all urls on page
        urls = tree.xpath('//@href')

        # If this page does not have any urls, return to starting page
        # TODO: Return to previous page instead of going to starting page.
        if len(urls) == 0:
            return self._start_url

        # Clean list of urls
        urls = clean_urls(current_url, urls)

        # Verify list of urls isn't empty
        if len(urls) == 0:
            return self._start_url

        # Pick random URL
        url = random.choice(urls)

        return url
