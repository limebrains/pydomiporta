#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from bs4 import BeautifulSoup

import domiporta
import domiporta.utils

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
    if url is None:
        url = domiporta.utils.get_url(category, transaction_type, voivodeship, city, street, filters)

    page, max_number_page, offers = 1, None, []

    while max_number_page is None or page <= max_number_page:
        page_number = "PageNumber=" + str(page)
        join_param = '?' if '?' not in url else '&'

        page_url = "{0}{1}{2}".format(url, join_param, page_number)
        offers_urls, markup = get_offers_from_category(page_url)
        offers += offers_urls

        if page == 1:
            max_number_page = domiporta.utils.get_max_number_page(markup)
        # assert False

        page += 1

    return offers


def get_offers_from_category(url):
    """ Parses available offer urls from given category from given page

    :param url: Defined url for Domiporta page with offers
    :type url: str
    :return: List of urls from given page
    :rtype: list
    """
    markup = BeautifulSoup(domiporta.utils.get_content_from_source(url), 'html.parser')
    offers_urls = []
    offers = markup.find_all('div', class_='detail-card')
    for offer in offers:
        offers_urls.append(offer.find('a').get('href'))
    return offers_urls, markup
