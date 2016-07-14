# -*- coding: utf-8 -*-

import unittest

from store import Store


class TestStore(unittest.TestCase):

    def test_base(self):
        store = Store("/tmp/test_file_store.json")

        store.save('some_site', {'title': 'Success!'})

        self.assertEqual({'title': 'Success!'},
                         store.get('some_site'))
