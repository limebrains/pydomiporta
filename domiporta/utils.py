#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from . import BASE_URL
from scrapper_helpers.utils import replace_all, get_random_user_agent, caching, key_md5

log = logging.getLogger(__file__)


def get_max_number_page(url):
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    max_number = markup.find(class_='pagination__separator').next.next.next.text
    return int(max_number)


def get_url(category='nieruchomosci', transaction_type='wszystkie', voivodeship=None,
            city=None, street=None, **filters):
    return 'url'


@caching(key_func=key_md5)
def get_content_from_source(url):
    """ Connects with given url

    If environmental variable DEBUG is True it will cache response for url in /var/temp directory

    :param url: Website url
    :type url: str
    :return: Response for requested url
    """
    response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        log.warning('Request for {0} failed. Error: {1}'.format(url, e))
        return None
    return response.content
