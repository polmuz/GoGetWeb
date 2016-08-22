# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from scraping import get_webpage_content, extract_xpaths, Not200Exception


class TestGetWebpageContent(unittest.TestCase):

    @patch('scraping.requests.get')
    def test_base(self, requests_get_mock):
        expected_content = b'<h1>Chuck Norris</h1>'

        requests_get_mock.return_value = MagicMock(
            content=expected_content,
            status_code=200
        )

        content = get_webpage_content("http://test.url")

        self.assertEqual(expected_content, content)

    @patch('scraping.requests.get')
    def test_status_not_ok(self, requests_get_mock):

        requests_get_mock.return_value = MagicMock(
            content=b'Not Found',
            status_code=404
        )

        with self.assertRaises(Not200Exception):
            content = get_webpage_content("http://test.url")

    @patch('scraping.requests.get')
    def test_requests_exception(self, requests_get_mock):
        requests_get_mock.side_effect = Exception("Requests Exception!")

        with self.assertRaises(Exception):
            content = get_webpage_content("http://test.url")



class TestExtractXpath(unittest.TestCase):

    def test_base(self):

        content = """
        <html>
          <body>
            <h1>Title!</h1>
            <p>Bla</p>
          </body>
        </html>
        """

        xpaths = {
            "title": "//h1"
        }

        extracted = extract_xpaths(content, xpaths)

        self.assertEqual(extracted, {"title": "Title!"})


    def test_multiple_elements(self):

        content = """
        <html>
          <body>
            <h1>Title!</h1>
            <p>Bla</p>
            <p>Ble</p>
          </body>
        </html>
        """

        xpaths = {
            "description": "//p"
        }

        extracted = extract_xpaths(content, xpaths)

        self.assertEqual(extracted, {"description": "Bla\nBle"})
