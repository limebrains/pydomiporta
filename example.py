import json

from domiporta.category import get_category, get_offers_from_category
# from domiporta.offer import get_offer_data
from domiporta.utils import get_max_number_page, get_url

url = 'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdynia/srodmiescie?Pietro.From=4'
url_gdansk = 'http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk?Pietro.From=4&Pietro.To=6'

# offers_urls = get_category(None, 'Mieszkania', 'wynajme', 'Pomorskie', 'Gdańsk', filters={'Pietro.From': 4, 'Pietro.To': 6})
offers_urls = get_category(url)
for i, url_from_offer in enumerate(offers_urls):
    print(str(i) + ": " + url_from_offer)
print(len(offers_urls))

# with open('test_data/output.json', 'w') as output_file:
#     output_file.write('[')
#     for urls_from_offers in offers:
#         data = get_offer_data(urls_from_offers)
#         # print(data)
#         output_file.write(json.dumps(data) + ',\n')
#     output_file.write(']')
