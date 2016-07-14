# -*- coding: utf-8 -*-

import os
import json

class Store():

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                content = f.read()
                if content:
                    data = json.loads(content)
                else:
                    data = {}
        else:
            data = {}

        return data

    def save_data(self, data):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(data))

    def get(self, key):
        data = self.get_data()
        return data.get(key)

    def save(self, key, value):
        data = self.get_data()
        data[key] = value
        self.save_data(data)
