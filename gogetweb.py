# -*- coding: utf-8 -*-

import sys
import json
import logging

from store import Store

from scraping import scrap_profile


def load_profiles(file_name):
    with open(file_name) as f:
        profiles = json.loads(f.read())

    return profiles


def compare_contents(profile_name, config, store):
    old_version = store.get(profile_name)

    data = scrap_profile(profile_name, config)

    if old_version and old_version != data:
        logging.info("{}: New data!".format(profile_name))
        logging.info(data)
        store.save(profile_name, data)

    elif not old_version:
        logging.info("{}: Data saved for the first time!".format(profile_name))
        logging.info(data)
        store.save(profile_name, data)

    else:
        logging.info("{}: No changes".format(profile_name))


def get_web(profiles_file_name, store_file_name):
    profiles = load_profiles(profiles_file_name)

    store = Store(store_file_name)

    for name, config in profiles.items():
        compare_contents(name, config, store)


if __name__ == "__main__":
    profiles_file_name = sys.argv[1]
    store_file_name = sys.argv[2]

    get_web(profiles_file_name, store_file_name)
