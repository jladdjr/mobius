# !/usr/bin/env python

#  Ignore lowercase constant names (in bottom section)
#  pylint: disable=C0103

#  Ignore protected access to private methods
#  pylint: disable=W0212

"""
Web Crawler test.
"""

import unittest
import xmlrunner

from mock import (Mock, PropertyMock, patch)
import requests

from mobius.mobius.web_crawler.parser import getParsedPage


class WebCrawlerTest(unittest.TestCase):
    """
    Tests Web Crawler.
    """

    # Create a mock class for Response
    @patch('requests.models.Response')
    def test_getParsedPage(self, MockResponseClass):
        """
        Test getParsedPage() method.

        :param MockResponseClass: Mock of request's Response class.
        """
        # Create a mock requests.Response object
        # (This allows us to simulate requesting a webpage)
        mockResponse = MockResponseClass()
        type(mockResponse).status_code = PropertyMock(return_value=200)
        type(mockResponse).headers = \
            PropertyMock(return_value={'content-type': 'text/html'})
        type(mockResponse).text = \
            PropertyMock(return_value="""\
<html>
<head><title>Mock webpage</title></head>
<body>
<h1>Mock webpage</h1><p />
<a href="http://mock.com/another/page.htm">Mock link</a>
</body>
</html>
""")

        # Mock get method (to return mock response)
        requests.get = Mock(return_value=mockResponse)

        # Test method
        url = 'http://mock.com'
        parsedPage = getParsedPage(url)

        # Get page title from parsed page
        results = parsedPage.xpath("/html/head/title/text()")
        self.assertEqual(len(results), 1)
        title = results[0]
        self.assertEqual(title, "Mock webpage")

        # Get url from parsed page
        results = parsedPage.xpath("/html/body/a/@href")
        self.assertEqual(len(results), 1)
        href = results[0]
        self.assertEqual(href, "http://mock.com/another/page.htm")

if __name__ == '__main__':
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    suite = unittest.TestLoader().loadTestsFromTestCase(WebCrawlerTest)
    testResult = xmlrunner.XMLTestRunner(output='test-reports').run(suite)
    failures_and_errors = len(testResult.failures) + len(testResult.errors)
    exit(failures_and_errors)
