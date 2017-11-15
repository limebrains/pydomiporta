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
])
def test_get_url(args, filters, url):
    assert domiporta.utils.get_url(*args, filters=filters) == url
