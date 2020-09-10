
import json

from mobile_de.scraper import *
from scalg import score

from settings import _MAKESJSON

def search(search_params : list) -> list:

    makes_dict = load_makes('mobile_de')
    current_url, pagesnr = search_url(makes_dict, search_params)

    # get links
    car_links = []
    for i in range(pagesnr - 1):
        for link in get_car_links(current_url):
            car_links.append(link)
        current_url = next_page(current_url, i + 1)

    assert len(car_links) == 0

    data = [get_car_data(link) for link in car_links]
    #data = score(source_data : list, weights : list, *args)
    
    return data

# existing searches checker
def checker(data : list) -> list:

    car_urls = [d[0] for d in data if not d[0] in car_urls]
    for link in car_urls:
        new_price = check_car_price(link)
        if not new_price == data[data.index(link)][1]:
            data[data.index(link)][1] = new_price

    return data

def load_makes(website : str) -> dict:
    with open(_MAKESJSON, 'r', encoding="utf-8", newline='') as mjson:
        data = mjson.read()
        makes_dict = (json.loads(data))
        makes_dict = makes_dict[website]
    return makes_dict
