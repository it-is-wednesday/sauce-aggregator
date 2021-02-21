#!/usr/bin/env python3

import argparse
import re
from urllib.parse import urlparse

import linkpreview
import requests
from colorama import Fore


titles_to_ignore = [
    None,
    "SVG namespace",
    "XLink namespace",
    "WhatsApp Web",
    "Schema.org",
    "ns"
]


def print_link(title, link, is_colored):
    print(title)

    if is_colored:
        print(Fore.MAGENTA, end="")
    print("-" * len(title))

    if is_colored:
        print(Fore.YELLOW, end="")
    print(link)

    if is_colored:
        print(Fore.RESET, end="")
    print("\n")


def links_in_page(page: str, excluded_domain: str):
    excluded_domain = excluded_domain\
        .replace("www.", "").replace("http://", "").replace("https://", "")

    for match in re.compile(r"\"https?://(?:www\.)?(.*?)\"").finditer(page):
        if not match.group(1).startswith(excluded_domain):
            yield match.group(0).strip("\"")


def main(article_url, is_colored=True):
    domain = urlparse(article_url).netloc
    page = requests.get(article_url).text

    for link in links_in_page(page, domain):
        try:
            preview = linkpreview.link_preview(link)
            if preview.title in titles_to_ignore:
                continue
            title = preview.title
        except requests.HTTPError:
            title = "Untitled"

        print_link(title, link, is_colored)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument("url")
    parser.add_argument("--no-color", action="store_true")
    args = parser.parse_args()
    main(args.url, not args.no_color)
