import json

from domiporta.category import get_category, get_offers_from_category
# from domiporta.offer import get_offer_data
from domiporta.utils import get_max_number_page

# offers = get_category(None, 'mieszkania', 'Sopot', transaction_type='do-wynajecia')
# offers = get_category(url=url)

print("'" + str(get_max_number_page('http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdansk/przymorze')) + "'")

print(get_offers_from_category('http://www.domiporta.pl/mieszkanie/wynajme/pomorskie/gdynia/witomino'))

# with open('test_data/output.json', 'w') as output_file:
#     output_file.write('[')
#     for urls_from_offers in offers:
#         data = get_offer_data(urls_from_offers)
#         # print(data)
#         output_file.write(json.dumps(data) + ',\n')
#     output_file.write(']')
