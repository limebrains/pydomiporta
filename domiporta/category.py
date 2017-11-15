#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
from .utils import get_url, get_max_number_page, get_content_from_source

log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def get_category(url=None, category='nieruchomosci', transaction_type='wszystkie', voivodeship=None, city=None,
                 street=None, filters=None):
    """

    :param url:
    :param category:
    :param transaction_type:
    :param voivodeship:
    :param city:
    :param street:
    :param filters:
    :return:
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
        print(page_url)
        offers_urls = get_offers_from_category(page_url)
        for offer_url in offers_urls:
            offers.append(offer_url)
    return offers


def get_offers_from_category(url):
    """

    :param url:
    :return:
    """
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    offers_urls = []
    offers = markup.find_all('div', class_='detail-card')
    for offer in offers:
        offers_urls.append(offer.find('a').get('href'))
    return offers_urls
