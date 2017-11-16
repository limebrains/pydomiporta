#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from bs4 import BeautifulSoup

from .utils import get_content_from_source, get_max_number_page, get_url

log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def get_category(url=None, category='nieruchomosci', transaction_type='wszystkie', voivodeship=None, city=None,
                 street=None, filters=None):
    """ Parses available offer urls from given category search page

    :param url: Url to search web page
    :param category: Type of property of interest (Mieszkanie/Dom/Garaż/Działka)
    :param transaction_type: Type of transaction
    :param voivodeship: Voivodeship
    :param city: City
    :param street: Street
    :param filters: Dictionary with additional filters
    :type url: str, None
    :type category:str, None
    :type transaction_type: str, None
    :type voivodeship: str, None
    :type city: str, None
    :type street: str, None
    :type filters: dict, None
    :return: List of urls of all offers for given parameters
    :rtype: list
    """
    if not url:
        url = get_url(category, transaction_type, voivodeship, city, street, filters)
    max_number_page = get_max_number_page(url)
    offers = []
    for i in range(1, max_number_page + 1):
        page_url = url
        if i > 1:
            if '?' not in url:
                page_url += "?"
            else:
                page_url += "&"
            page_url += "PageNumber=" + str(i)
        offers_urls = get_offers_from_category(page_url)
        for offer_url in offers_urls:
            offers.append(offer_url)
    return offers


def get_offers_from_category(url):
    """ Parses available offer urls from given category from given page

    :param url: Defined url for Domiporta page with offers
    :type url: str
    :return: List of urls from given page
    :rtype: list
    """
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    offers_urls = []
    offers = markup.find_all('div', class_='detail-card')
    for offer in offers:
        offers_urls.append(offer.find('a').get('href'))
    return offers_urls
