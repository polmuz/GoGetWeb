# -*- coding: utf-8 -*-

import requests

import lxml.html


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


def scrap_profile(name, config):
    content = get_webpage_content(config['url'])
    return extract_xpaths(content, config['extract'])
