#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from bs4 import BeautifulSoup
from scrapper_helpers.utils import finder

from .utils import get_content_from_source


@finder(False, class_='detail-feature__name', text='Liczba pokoi: ')
def get_rooms_for_offer(item, *args, **kwargs):
    """ Parse information about numbers of rooms

    :param item: Tag html found by finder in html markup
    :return: Number of rooms or None if information not given
    :rtype: int, None
    """
    if not item:
        return None
    rooms = item.find_next_sibling().text
    return int(rooms)


@finder(False, class_='detail-feature__name', text='Piętro: ')
def get_floor_for_offer(item, *args, **kwargs):
    """ Parse information about number of the floor

    :param item: Tag html found by finder in html markup
    :return: Number of the floor or None if information not given
    :rtype: int, None
    """
    if not item:
        return None
    floor = item.find_next_sibling().text
    if floor == 'Parter':
        return 0
    return int(floor)


@finder(False, class_='details-gallery-thumbnails')
def get_images_for_offer(item, *args, **kwargs):
    """ Parse images from offer

    :param item: Tag html found by finder in html markup
    :return: List of image urls
    :rtype: list
    """
    images_links = []
    if item:
        images = item.find_all('img')
        for img in images:
            images_links.append(img.get('src').replace('search-results', 'original'))
    return images_links


@finder(False, class_='details-description__full')
def get_description_for_offer(item, *args, **kwargs):
    """ Parse description of offer

    :param item: Tag html found by finder in html markup
    :return: description of offer
    :rtype: str
    """
    return item.text


def get_meta_data(markup):
    """ parse meta data

    :param markup: raw html
    :return: dictionary with data
    :rtype: dict
    """
    data = str(markup).split('setContactFormData(')[1].split(');')[0]
    data = json.loads(data)
    return data


def get_gps_data(content):
    """ Parse latitude and longitude

    :param content: raw html
    :return: list with geographical coordinates or None if can't find
    :rtype: list
    """
    try:
        return str(content).split('showMapDialog(')[1].split(')')[0].split(', ')[:2]
    except IndexError:
        print('not found')
        return None


def get_offer_data(url):
    """ Parse details about given offer

    :param url: Url to offer web page
    :type url: str
    :return: Details about given offer
    :rtype: dict
    """
    content = get_content_from_source(url)
    markup = BeautifulSoup(content, 'html.parser')
    meta_data = get_meta_data(markup)
    print(url)

    return {
        'id': meta_data.get('AdvertId'),
        'price': float(meta_data.get('AdvertPrice')),
        'surface': float(meta_data.get('AdvertMeters').replace(',', '.')),
        'rooms': get_rooms_for_offer(markup),
        'floor': get_floor_for_offer(markup),
        'voivodeship': meta_data.get('AdvertRegion'),
        'city': meta_data.get('AdvertCity'),
        'district': meta_data.get('AdvertDistrict'),
        'street': meta_data.get('AdvertStreet'),
        'phone': meta_data.get('ContactPhone'),
        'gps': get_gps_data(content),
        'images': get_images_for_offer(markup),
        'description': get_description_for_offer(markup),
        'url': url
    }
