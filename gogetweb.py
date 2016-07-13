# -*- coding: utf-8 -*-

import requests


class Not200Exception(Exception): pass


def get_webpage_content(url):
    r = requests.get(url)

    if r.status_code == 200:
        return r.content

    raise Not200Exception(
        "Failed to get webpage {}, status: {}".format(url, r.status_code)
    )


if __name__ == "__main__":
    c = get_webpage_content("https://en.wikipedia.org/wiki/Chuck_Norris")
    print(c[:50])
