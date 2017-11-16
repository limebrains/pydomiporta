import sys

import domiporta
import domiporta.category
import domiporta.offer
import domiporta.utils
import pytest

if sys.version_info < (3, 3):
    from mock import mock
else:
    from unittest import mock


@pytest.mark.parametrize('args, filters, url', [
    (('Mieszkanie', 'wynajme', 'Pomorskie', 'Gdańsk'), {'Pietro.From': 4, 'Pietro.To': 6},
     'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk?Pietro.From=4&Pietro.To=6'),
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
    with mock.patch('domiporta.utils.get_content_from_source') as get_content:
        get_content.return_value = offers_search_markup
        assert domiporta.utils.get_max_number_page('') == 1


def test_get_categoy(offers_search_markup):
    with mock.patch('domiporta.utils.get_content_from_source') as get_content:
        with mock.patch('domiporta.utils.get_max_number_page') as get_max_page:
            get_max_page.return_value = 1
            get_content.return_value = offers_search_markup
            assert isinstance(domiporta.category.get_category(
                url='http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk'), type([]))
