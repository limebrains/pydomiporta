import sys

import domiporta
import domiporta.category
import domiporta.offer
import domiporta.utils
import pytest
from bs4 import BeautifulSoup

if sys.version_info < (3, 3):
    from mock import mock
else:
    from unittest import mock


@pytest.mark.parametrize('args, filters, url', [
    (('Mieszkanie', 'wynajme', 'Pomorskie', 'Gdańsk'), {'Pietro.From': 4, 'Pietro.To': 6},
     'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk?Pietro.From=4&Pietro.To=6'),
    (('Dom', 'sprzedam', 'Mazowieckie', 'Warszawa', 'Białołęka'), {},
     'http://www.domiporta.pl/dom/sprzedam/mazowieckie/warszawa/bialoleka')
])
def test_get_url(args, filters, url):
    assert domiporta.utils.get_url(*args, filters=filters) == url


@pytest.fixture
def offer_markup():
    with open('test_data/offer_page.htm', 'r') as page:
        return page.read()


@pytest.fixture
def offers_search_markup():
    with open('test_data/offers_search_page.htm', 'r') as page:
        return page.read()


def test_get_offer_data(offer_markup):
    with mock.patch('domiporta.utils.get_content_from_source') as get_content:
        get_content.return_value = offer_markup
        assert isinstance(domiporta.offer.get_offer_data(
            'http://www.domiporta.pl/nieruchomosci/wynajme-mieszkanie-dwupokojowe-gdynia-srodmiescie--45m2/147697257'),
            type({})
        )


def test_get_max_page(offers_search_markup):
    assert domiporta.utils.get_max_number_page(BeautifulSoup(offers_search_markup, 'html.parser')) == 1


@pytest.mark.parametrize('args', [('url=None','Mieszkanie', 'Wynajme', 'Pomorskie', 'Gdańsk')])
def test_get_categoy(offers_search_markup, args):
    with mock.patch('domiporta.utils.get_content_from_source') as get_content:
        with mock.patch('domiporta.utils.get_max_number_page') as get_max_page:
            get_max_page.return_value = 1
            get_content.return_value = offers_search_markup
            assert isinstance(domiporta.category.get_category(*args), type([]))


def test_get_category_pages(offers_search_markup):
    with mock.patch('domiporta.utils.get_content_from_source') as get_content:
        with mock.patch('domiporta.utils.get_max_number_page') as get_max_page:
            with mock.patch('domiporta.category.get_offers_from_category') as get_offers:
                expected_pages = 4
                offers_per_page = ['1', '2']
                category_url = 'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk?Pietro.From=2'

                get_offers.return_value = offers_per_page, offers_search_markup
                get_max_page.return_value = expected_pages
                get_content.return_value = offers_search_markup

                all_offers = domiporta.category.get_category(url=category_url)

                assert len(all_offers) == expected_pages * len(offers_per_page)
