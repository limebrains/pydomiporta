Introduction
============
pydomiporta supplies two methods that can be used to scrape data from Domiporta website

.. _categories:

======================
Scraping category data
======================
This method scrapes available offer urls from Domiporta search results with parameters
.. autofunction:: domiporta.category.get_category

The function above can be used like this:

::

    filters = {'Price.From': 1500, 'Pietro.To': 3}
    offer_urls = domiporta.category.get_category(url=None, 'Mieszkania', 'wynajme', 'Pomorskie', 'Gdańsk', filters)

The code above will put a list of urls containing all apartments found in the given category into the offers_url variable

===================
Scraping offer data
===================
This method scrapes details of offer
.. autofunction:: domiporta.offer.get_offer_data

The function above can be used like this:

::

    details = domiporta.offer.get_offer_data(url)

the code above will create dictionary with details of offer from given url
