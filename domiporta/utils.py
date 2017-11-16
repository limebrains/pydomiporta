#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import requests
from bs4 import BeautifulSoup
from scrapper_helpers.utils import caching, get_random_user_agent, key_md5, replace_all

from . import BASE_URL

log = logging.getLogger(__file__)
POLISH_CHARACTERS_MAPPING = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z"}


def encode_text_to_html(text):
    """ Change text to lower cases, gets rid of polish characters replacing them with simplified version,
    replaces spaces with dashes

    :param text: text to encode
    :type text: str
    :return: encoded text which can be used in url
    :rtype: str
    """
    replace_dict = POLISH_CHARACTERS_MAPPING
    replace_dict.update({' ': '-'})
    return replace_all(text.lower(), replace_dict)


def get_max_number_page(url):
    """ Parse number of pages for search result

    :param url:
    :return:
    """
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    max_number = markup.find(class_='pagination__separator').next.next.next.text
    return int(max_number)


def get_url(category='nieruchomosci', transaction_type='wszystkie', voivodeship=None,
            city=None, street=None, filters=None):
    """ Create url to Domiporta search web page with given parameters and filters

    :param category: Type of property of interest (Mieszkanie/Dom/Garaż/Działka)
    :param transaction_type: Type of transaction
    :param voivodeship: Voivodeship
    :param city: City
    :param street: Street
    :param filters: Dictionary with additional filters
    :type category:str, None
    :type transaction_type: str, None
    :type voivodeship: str, None
    :type city: str, None
    :type street: str, None
    :type filters: dict, None
    :return: Url to Domiporta search web page
    :rtype: str
    """
    url = BASE_URL + encode_text_to_html(category) + "/" + encode_text_to_html(transaction_type)
    if voivodeship:
        url += "/" + encode_text_to_html(voivodeship)
        if city:
            url += "/" + encode_text_to_html(city)
            if street:
                url += "/" + encode_text_to_html(street)
    if filters and len(filters) > 0:
        for i, param in enumerate(filters):
            if i == 0:
                url += "?"
            else:
                url += "&"
            url += "{0}={1}".format(param, filters[param])
    return url


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
