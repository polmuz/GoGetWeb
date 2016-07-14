# -*- coding: utf-8 -*-

import sys
import json

import requests

import lxml.html

from store import Store


class Not200Exception(Exception): pass


def get_webpage_content(url):
    r = requests.get(url)

    if r.status_code == 200:
        return r.content

    raise Not200Exception(
        "Failed to get webpage {}, status: {}".format(url, r.status_code)
    )


def extract_xpaths(content, xpaths):
    html = lxml.html.fromstring(content)

    extracted = {}

    for key, xpath in xpaths.items():
        # Get all the text in the selected node, concatenate it.
        # Then join all the results using new lines
        extracted[key] = "\n".join(
            ["".join(e.xpath(".//text()")) for e in html.xpath(xpath)]
        )

    return extracted


def fetch_profile(name, config):
    content = get_webpage_content(config['url'])
    return extract_xpaths(content, config['extract'])


def load_profiles(file_name):
    with open(file_name) as f:
        profiles = json.loads(f.read())

    return profiles


def compare_contents(profile_name, config, store):
    old_version = store.get(profile_name)

    data = fetch_profile(profile_name, config)

    if old_version and old_version != data:
        print("{}: New data!".format(profile_name))
        print(data)
        store.save(profile_name, data)

    elif not old_version:
        print("{}: Data saved for the first time!".format(profile_name))
        print(data)
        store.save(profile_name, data)

    else:
        print("{}: No changes".format(profile_name))


if __name__ == "__main__":
    profiles_file_name = sys.argv[1]
    profiles = load_profiles(profiles_file_name)

    store = Store(sys.argv[2])

    for name, config in profiles.items():
        compare_contents(name, config, store)
