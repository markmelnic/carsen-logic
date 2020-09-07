
from scraper import *
from test import load_makes

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

    return data
