#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re
import datetime as dt
from .utils import get_content_from_source
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all, finder


@finder(False, class_='detail-feature__name', text='Liczba pokoi: ')
def get_rooms_for_offer(item, *args, **kwargs):
    if not item:
        return None
    rooms = item.find_next_sibling().text
    return int(rooms)


@finder(False, class_='detail-feature__name', text='Piętro: ')
def get_floor_for_offer(item, *args, **kwargs):
    floor = item.find_next_sibling().text
    if floor == 'Parter':
        return 0
    return int(floor)


@finder(False, class_='details-gallery-thumbnails')
def get_images_for_offer(item, *args, **kwargs):
    images_links = []
    if item:
        images = item.find_all('img')
        for img in images:
            images_links.append(img.get('src').replace('search-results', 'original'))
    return images_links


@finder(False, class_='details-description__full')
def get_description_for_offer(item, *args, **kwargs):
    return item.text


def get_meta_data(markup):
    data = str(markup).split('setContactFormData(')[1].split(');')[0]
    data = json.loads(data)
    return data


def get_gps_data(content):
    try:
        return str(content).split('showMapDialog(')[1].split(')')[0].split(', ')[:2]
    except IndexError:
        print('not found')


def get_offer_data(url):
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
