# -*- coding: utf-8 -*-
from lxml import html
import requests
from urllib3.exceptions import LocationParseError  # Thrown by requests


def get_parsed_page(url):
    """
    * Requests page at url.
    * Parses web page.
    * Returns parsed page (as lxml.html object)

    :param url: URL for page
    :returns:   Parsed page (lxml.html object)
    """
    # Get page
    # TODO: Handle timeouts (What is a reasonable timeout?)
    req = None
    short_url = (url[:48] + '..') if len(url) > 50 else url  # Used in errors
    # See requests exceptions:
    #  pylint: disable=C0301
    # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    try:
        req = requests.get(url)
    except LocationParseError:
        print("   Malformed URL: {0}".format(short_url))
        return None
    except requests.exceptions.Timeout:
        print("   Timed out requesting page: {0}".format(short_url))
        return None
    except requests.exceptions.ConnectionError:
        print("   Network error while connecting with page: {0}".format(short_url))
        return None
    except requests.exceptions.HTTPError:
        print("   Invalid HTTP response: {0}".format(short_url))
        return None
    except requests.exceptions.TooManyRedirects:
        print("   Too many redirects: {0}".format(short_url))
        return None

    # Verify page could be reached
    #  pylint: disable=E1101
    if req.status_code != requests.codes.ok:
        print("   Error reading page ({0}): {1}".format(req.status_code, short_url))
        return None

    # Verify page is readable
    content_type = req.headers['content-type'].lower()
    if content_type.find('text/html') == -1 and \
            content_type.find('application/xhtml+xml') != -1:
        print("   Invalid content-type ({0}): {1}".format(content_type, short_url))
        return None

    text = req.text

    # Parse page
    try:
        tree = html.fromstring(text)
    except ValueError:
        print("   Unable to parse page: {0}".format(short_url))
        return None

    return tree
