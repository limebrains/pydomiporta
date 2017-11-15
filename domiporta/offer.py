#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re
import datetime as dt
from .utils import get_content_from_source
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all, finder


@finder(False, class_='detail-feature__value detail-feature__value--price')
def get_price_for_offer(item, *args, **kwargs):
    price = replace_all(item.text, {'\xa0': '', 'zł': ''})
    return float(price)


@finder(False, class_='detail-feature__name', text='Powierzchnia całkowita:')
def get_surface_area_for_offer(item, *args, **kwargs):
    area = re.match(r'\d+', item.find_next_sibling().text).group(0)
    return float(area)


@finder(False, class_='detail-feature__name', text='Liczba pokoi: ')
def get_rooms_for_offer(item, *args, **kwargs):
    rooms = item.find_next_sibling().text
    return int(rooms)


@finder(False, class_='detail-feature__name', text='Piętro: ')
def get_floor_for_offer(item, *args, **kwargs):
    floor = item.find_next_sibling().text
    if floor == 'Parter':
        return 0
    return int(floor)


@finder(False, class_='detail-feature__value detail-feature--full-localization')
def get_location_for_offer(item, *args, **kwargs):
    location = item.find_all('a')
    return location


def get_voivodeship_for_offer(markup):
    voivodeship = get_location_for_offer(markup)[0].text
    return voivodeship


def get_city_for_offer(markup):
    city = get_location_for_offer(markup)[1].text
    return city


def get_street_for_offer(markup):
    street = get_location_for_offer(markup)[-1].text
    if not street:
        return None
    return street


def get_meta_data(markup):
    data = str(markup).split('setContactFormData(')[1].split(');')[0]
    data = json.loads(data)
    return data


def get_offer_data(url):
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    meta_data = get_meta_data(markup)

    return {
        'phone': meta_data.get('ContactPhone'),
        'price': get_price_for_offer(markup),
        'surface': get_surface_area_for_offer(markup),
        'rooms': get_rooms_for_offer(markup),
        'floor': get_floor_for_offer(markup),
        'voivodeship': get_voivodeship_for_offer(markup),
        'city': get_city_for_offer(markup),
        'street': get_street_for_offer(markup)
    }
