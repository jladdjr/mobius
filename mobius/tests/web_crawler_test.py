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

from mobius.mobius.web_crawler.parser import get_parsed_page


class WebCrawlerTest(unittest.TestCase):
    """
    Tests Web Crawler.
    """

    # Create a mock class for Response
    @patch('requests.models.Response')
    def test_get_parsed_page(self, MockResponseClass):
        """
        Test get_parsed_page() method.

        :param MockResponseClass: Mock of request's Response class.
        """
        # Create a mock requests.Response object
        # (This allows us to simulate requesting a webpage)
        mock_response = MockResponseClass()
        type(mock_response).status_code = PropertyMock(return_value=200)
        type(mock_response).headers = \
            PropertyMock(return_value={'content-type': 'text/html'})
        type(mock_response).text = \
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
        requests.get = Mock(return_value=mock_response)

        # Test method
        url = 'http://mock.com'
        parsed_page = get_parsed_page(url)

        # Get page title from parsed page
        results = parsed_page.xpath("/html/head/title/text()")
        self.assertEqual(len(results), 1)
        title = results[0]
        self.assertEqual(title, "Mock webpage")

        # Get url from parsed page
        results = parsed_page.xpath("/html/body/a/@href")
        self.assertEqual(len(results), 1)
        href = results[0]
        self.assertEqual(href, "http://mock.com/another/page.htm")


if __name__ == '__main__':
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    suite = unittest.TestLoader().loadTestsFromTestCase(WebCrawlerTest)
    test_result = xmlrunner.XMLTestRunner(output='test-reports').run(suite)
    failures_and_errors = len(test_result.failures) + len(test_result.errors)
    exit(failures_and_errors)
