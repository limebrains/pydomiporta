import json

from domiporta.category import get_category
from domiporta.offer import get_offer_data

url = 'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdynia/srodmiescie?Pietro.From=4'

offers_urls = get_category(url)

with open('test_data/output.json', 'w') as output_file:
    output_file.write('[\n')
    for urls_from_offers in offers_urls:
        data = get_offer_data(urls_from_offers)
        print(data)
        output_file.write(json.dumps(data) + ',\n')
    output_file.write(']')
