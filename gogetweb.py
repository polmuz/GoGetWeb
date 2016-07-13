import unittest
from unittest.mock import patch, MagicMock

import requests


class Not200Exception(Exception): pass


def get_webpage_content(url):
    r = requests.get(url)

    if r.status_code == 200:
        return r.content

    raise Not200Exception(
        "Failed to get webpage {}, status: {}".format(url, r.status_code)
    )


class TestGetWebpageContent(unittest.TestCase):

    @patch('requests.get')
    def test_base(self, requests_get_mock):
        expected_content = b'<h1>Chuck Norris</h1>'

        requests_get_mock.return_value = MagicMock(
            content=expected_content,
            status_code=200
        )

        content = get_webpage_content("http://test.url")

        self.assertEqual(expected_content, content)

    @patch('requests.get')
    def test_status_not_ok(self, requests_get_mock):

        requests_get_mock.return_value = MagicMock(
            content=b'Not Found',
            status_code=404
        )

        with self.assertRaises(Not200Exception):
            content = get_webpage_content("http://test.url")

    @patch('requests.get')
    def test_requests_exception(self, requests_get_mock):
        requests_get_mock.side_effect = Exception("Requests Exception!")

        with self.assertRaises(Exception):
            content = get_webpage_content("http://test.url")


if __name__ == "__main__":
    c = get_webpage_content("https://en.wikipedia.org/wiki/Chuck_Norris")
    print(c[:50])
