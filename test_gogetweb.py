# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from gogetweb import get_webpage_content, Not200Exception


class TestGetWebpageContent(unittest.TestCase):

    @patch('gogetweb.requests.get')
    def test_base(self, requests_get_mock):
        expected_content = b'<h1>Chuck Norris</h1>'

        requests_get_mock.return_value = MagicMock(
            content=expected_content,
            status_code=200
        )

        content = get_webpage_content("http://test.url")

        self.assertEqual(expected_content, content)

    @patch('gogetweb.requests.get')
    def test_status_not_ok(self, requests_get_mock):

        requests_get_mock.return_value = MagicMock(
            content=b'Not Found',
            status_code=404
        )

        with self.assertRaises(Not200Exception):
            content = get_webpage_content("http://test.url")

    @patch('gogetweb.requests.get')
    def test_requests_exception(self, requests_get_mock):
        requests_get_mock.side_effect = Exception("Requests Exception!")

        with self.assertRaises(Exception):
            content = get_webpage_content("http://test.url")
