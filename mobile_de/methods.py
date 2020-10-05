import json, scalg

from mobile_de.scraper import *
from settings import _MAKESJSON, TEST_MAKESJSON


# perform a detailed search of each listing
def search(search_params: list) -> list:
    makes_dict = load_makes("mobile_de")
    current_url, pagesnr = search_url(makes_dict, search_params)

    # get links
    car_links = []
    for i in range(pagesnr):
        for link in get_car_links(current_url):
            car_links.append(link)
        current_url = next_page(current_url, i + 1)

    assert len(car_links) != 0

    data = [get_car_data(link) for link in car_links]
    data = scalg.score_columns(data, [2, 3, 4], [1, 0, 0])

    return data


# perform a surface search for the generated url
def surface_search(search_params: list) -> list:
    makes_dict = load_makes("mobile_de")
    current_url, pagesnr = search_url(makes_dict, search_params)

    data = []
    for i in range(pagesnr):
        for item in surface_data(current_url):
            data.append(item)
        current_url = next_page(current_url, i + 1)

    assert data != []

    data = scalg.score_columns(data, [2, 3, 4], [1, 0, 0])

    return data


# existing searches checker
def checker(data: list) -> list:
    changed = False
    car_urls = [d[0] for d in data]
    for link in car_urls:
        new_price = check_car_price(link)
        if not float(new_price) == float(data[car_urls.index(link)][3]):
            changed = True
            data[car_urls.index(link)][3] = new_price

    assert changed == True
    return data


# load makes and models from json file
def load_makes(website: str) -> dict:
    try:
        with open(_MAKESJSON, "r", encoding="utf-8", newline="") as mjson:
            data = mjson.read()
            makes_dict = json.loads(data)
            makes_dict = makes_dict[website]
        return makes_dict

    except FileNotFoundError:
        with open(TEST_MAKESJSON, "r", encoding="utf-8", newline="") as mjson:
            data = mjson.read()
            makes_dict = json.loads(data)
            makes_dict = makes_dict[website]
        return makes_dict
