# -*- coding: utf-8 -*-
import re


def clean_urls(current_url, urls):
    """
    Cleans a list of URLs retrieved from web page. Returns a unique set of
    absolute URLs.

    :param current_url: Current url (including protocol)
    :param urls:        List of URLs (retrieved, using xpath, from a given
                        page)
    """
    # Convert list to set (to ensure uniqueness)
    urls = set(urls)

    # Create new set. Will add valid URLs to this set.
    clean_urls = set()

    # Get base url of current page (i.e. everything but path)
    base_url = ''

    double_slash_index = current_url.find('://')
    assert double_slash_index != -1, "_cleanURLS(): current_url missing protocol"

    slash_index = current_url.find('/', double_slash_index + 3)
    if slash_index == -1:
        base_url = current_url
    else:
        base_url = current_url[:slash_index]

    # Process urls
    for url in urls:
        # print("DEBUG: {0}".format(url))
        # pdb.set_trace()

        # Is this an empty string?
        if len(url) == 0:
            # print("Ignoring empty string")
            continue

        # Does xpath result begin with double-slash?
        # If so, replace with http protocol
        #  pylint: disable=C0301
        # http://stackoverflow.com/questions/9646407/two-forward-slashes-in-a-url-src-href-attribute
        if url.find('//') == 0:
            url = 'http://' + url[2:]

        # Is this an anchor?
        if url[0] == '#':
            # print("Ignoring anchor: {0}".format(url))
            continue

        # Is this a relative link to the current page?
        if url == '/' or url == '.':
            # print('Ignoring relative reference to current page')
            continue

        # TODO: Don't ignore relative paths
        if url[0] == '.':
            continue

        # Is this a reference to java script?
        if url.lower().find('javascript') != -1:
            # print("Ignoring java script: {0}".format(url))
            continue

        # Ensure that url is absolute:

        # Is this URL already absolute?
        if url.find('http://') == 0 or url.find('https://') == 0:
            pass
        # Does URL use another protocol? (If so, ignore)
        elif re.search(r":[^\d]+", url):
            continue
        # Is this a relative url?
        elif url[0] == '/':
            # make absolute
            url = base_url + url
        else:
            url = base_url + '/' + url

        # If url includes an extension, verify that it is useable
        last_slash_index = url.rfind('/')

        # If there is no slash (or slash apppears at end of url)
        if last_slash_index == -1 or last_slash_index == len(url) - 1:
            # No extension. Assume page is readable.
            clean_urls.add(url)
        else:
            # URL does include path. Check extension.
            page = url[last_slash_index + 1:]
            page = page.lower()

            if page.find('.htm') == -1 and \
                    page.find('.php') == -1 and \
                    page.find('.jsp') == -1 and \
                    page.find('.do') == -1 and \
                    page.find('.asp') == -1 and \
                    page.find('.aspx') == -1 and \
                    page.find('.jspx') == -1 and \
                    page.find('.xhtml') == -1:
                # print("Ignoring unrecognized webpage type: {0}".format(url))
                continue

            # Page has valid extension
            clean_urls.add(url)

    # Convert set back to list
    # TODO: Is this a good use of sets / lists?
    clean_urls = list(clean_urls)

    return clean_urls
