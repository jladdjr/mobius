#!/usr/bin/env python

"""
Simple web crawler.
"""

import random
import re
import requests
from urllib3.exceptions import LocationParseError   #Thrown by requests
from lxml import html 

class WebCrawler(object):
    """
    Web Crawler.
    """
    
    def __init__(self, startURL="http://en.wikipedia.org"):
        """
        Initializes WebCrawler object.
        
        :param startURL: First page web crawler visits.
        """
        self._startURL = startURL       #First page to index
        self._index = {}                #Index - maps page titles to URLs

    def run(self, numPages):
        """
        Starts web crawler.

        :param numPages: Number of pages web crawler visits. 
        """

        print "Indexing.."
        print ""

        #Begin with starting page 
        url = self._startURL

        #Keep track of previous url. Will return to this
        #if a page is unavailable (or unreadable)
        previousURL = url
       
        #Loop to index each page
        index = 0
        while index < numPages:
            print "%d: %s" % (index, url)

            #Parse page
            tree = self._getParsedPage(url)

            #Revert to previous page if page can't be parsed 
            if tree is None:
                url = previousURL
                tree = self._getParsedPage(url)

            #Index page
            self._processPage(url, tree)

            #Next page
            previousURL = url
            url = self._nextPage(url, tree)
            index += 1

        print ""
        print "-----------------------------------"
        print ""
        print "Results:"
        print ""

        #Print index
        self._printIndex()

    def _getParsedPage(self, url):
        """
        * Requests page at url. 
        * Parses web page.
        * Returns parsed page (as lxml.html object)

        :param url: URL for page
        :returns:   Parsed page (lxml.html object)
        """
        #Get page
        #TODO: Handle timeouts (What is a reasonable timeout?)
        req = None
        shortUrl = (url[:48] + '..') if len(url) > 50 else url  #Used in errors
        #See requests exceptions:
        # pylint: disable=C0301
        #http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        try:
            req = requests.get(url)
        except LocationParseError:
            print "   Malformed URL: ", shortUrl
            return None
        except requests.exceptions.Timeout:
            print "   Timed out requesting page: ", shortUrl
            return None
        except requests.exceptions.ConnectionError:
            print "   Network error while connecting with page: ", shortUrl
            return None
        except requests.exceptions.HTTPError:
            print "   Invalid HTTP response: ", shortUrl
            return None
        except requests.exceptions.TooManyRedirects:
            print "   Too many redirects: ", shortUrl
            return None

        #Verify page could be reached
        # pylint: disable=E1101
        if req.status_code != requests.codes.ok:
            print "   Error reading page (%s): %s" % (req.status_code, shortUrl)
            return None

        #Verify page is readable
        contentType = req.headers['content-type'].lower()
        if contentType.find('text/html') == -1 and \
                contentType.find('application/xhtml+xml') != -1:
            print "   Invalid content-type (%s): %s" % (contentType, shortUrl)
            return None

        text = req.text
        
        #Parse page
        try:
            tree = html.fromstring(text)
        except ValueError:
            print "   Unable to parse page: %s" % shortUrl
            return None

        return tree

    def _processPage(self, url, tree):
        """
        Indexes a given page.

        :param url:  URL for web page.
        :param tree: Tree representing parse web page. 
        """
        #Get title
        xpath = '/html/head/title/text()'
        title = tree.xpath(xpath)
        if title == None or len(title) == 0:
            #Ignore pages without a title
            return
        else:
            title = title[0].strip()  #Remove whitespace at beginning/end

        #Map title to url
        self._index[url] = title

    def _nextPage(self, currentURL, tree):
        """
        Retrieves next page to process.

        If given page does not contain any URLs, returns
        the starting URL.

        :param currentURL: Current url (including protocol)
        :param tree:       Tree representing parse web page. 
        :returns:          Randomly selected URL.
        """
        #Get all urls on page
        urls = tree.xpath('//@href')

        #If this page does not have any urls, return to starting page
        #TODO: Return to previous page instead of going to starting page.
        if len(urls) == 0:
            return self._startURL

        #Clean list of urls
        urls = self._cleanURLs(currentURL, urls)

        #Verify list of urls isn't empty
        if len(urls) == 0:
            return self._startURL

        #Pick random URL
        url = random.choice(urls)

        return url

    def _cleanURLs(self, currentURL, urls):
        """
        Cleans a list of URLs retrieved from web page. Returns a unique set of 
        absolute URLs.

        :param currentURL: Current url (including protocol)
        :param urls:       List of URLs (retrieved, using xpath, from a given 
                           page)
        """
        #Convert list to set (to ensure uniqueness)
        urls = set(urls)

        #Create new set. Will add valid URLs to this set.
        cleanURLs = set()
      
        #Get base url of current page (i.e. everything but path)
        baseURL = ''

        doubleSlashIndex = currentURL.find('://')
        assert doubleSlashIndex != -1, \
                "_cleanURLS(): currentURL missing protocol"

        slashIndex = currentURL.find('/', doubleSlashIndex + 3)
        if slashIndex == -1:
            baseURL = currentURL
        else:
            baseURL = currentURL[:slashIndex]


        #Process urls
        for url in urls:
            #print "DEBUG: ", url
            #pdb.set_trace()
            
            #Is this an empty string?
            if len(url) == 0:
                #print "Ignoring empty string"
                continue

            #Does xpath result begin with double-slash? 
            #If so, replace with http protocol
            # pylint: disable=C0301
            #http://stackoverflow.com/questions/9646407/two-forward-slashes-in-a-url-src-href-attribute
            if url.find('//') == 0:
                url = 'http://' + url[2:]

            #Is this an anchor?
            if url[0] == '#':
                #print "Ignoring anchor: ", url
                continue

            #Is this a relative link to the current page?
            if url == '/' or url == '.':
                #print 'Ignoring relative reference to current page'
                continue

            #TODO: Don't ignore relative paths
            if url[0] == '.':
                continue

            #Is this a reference to java script?
            if url.lower().find('javascript') != -1:
                #print "Ignoring java script: ", url
                continue

            #Ensure that url is absolute:

            #Is this URL already absolute?
            if url.find('http://') == 0 or url.find('https://') == 0:
                pass
            #Does URL use another protocol? (If so, ignore)
            elif re.search(r":[^\d]+", url):
                continue
            #Is this a relative url?
            elif url[0] == '/':
                #make absolute
                url = baseURL + url
            else:
                url = baseURL + '/' + url

            #If url includes an extension, verify that it is useable 
            lastSlashIndex = url.rfind('/')

            #If there is no slash (or slash apppears at end of url)
            if lastSlashIndex == -1 or \
                lastSlashIndex == len(url) - 1: 
                #No extension. Assume page is readable.
                cleanURLs.add(url)
            else:
                #URL does include path. Check extension.
                page = url[lastSlashIndex + 1:]
                page = page.lower()

                if page.find('.htm') == -1 and \
                        page.find('.php') == -1 and \
                        page.find('.jsp') == -1 and \
                        page.find('.do') == -1 and \
                        page.find('.asp') == -1 and \
                        page.find('.aspx') == -1 and \
                        page.find('.jspx') == -1 and \
                        page.find('.xhtml') == -1:
                    #print "Ignoring unrecognized webpage type: ", url
                    continue
                
                #Page has valid extension
                cleanURLs.add(url)

        #Convert set back to list
        #TODO: Is this a good use of sets / lists?
        cleanURLs = list(cleanURLs)

        return cleanURLs

    def _printIndex(self):
        """
        Prints index.
        """
        keys = sorted(self._index.keys())

        for key in keys:
            #Trunace / Pad key 
            formattedKey = (key[:48] + "..") if len(key) > 50 else key
            formattedKey = formattedKey.ljust(50)

            #Truncate title, Remove newlines
            title = self._index[key]
            formattedTitle = (title[:48] + "..") if len(title) > 50 else title
            formattedTitle = formattedTitle.replace('\n','')

            print "%s %s" % (formattedKey, formattedTitle)
