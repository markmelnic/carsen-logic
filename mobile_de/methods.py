import scalg

from mobile_de.scraper import *

# perform a detailed search of each listing
def search(search_params: list, db=False) -> list:
    if db:
        current_url, pagesnr, database = search_url(search_params, db)
    else:
        current_url, pagesnr = search_url(search_params, db)

    # get links
    car_links = []
    for i in range(pagesnr):
        for link in get_page_listings(current_url):
            car_links.append(link)
        current_url = next_page(current_url, i + 1)

    assert len(car_links) != 0

    data = [get_data(link) for link in car_links]
    data = scalg.score_columns(data, [2, 3, 4], [0, 1, 0])

    if db:
        return database, data
    else:
        return data


# perform a surface search for the generated url
def surface_search(search_params: list, db=False) -> list:
    if db:
        current_url, pagesnr, database = search_url(search_params, db)
    else:
        current_url, pagesnr = search_url(search_params, db)

    data = []
    for i in range(pagesnr):
        for item in surface_data(current_url):
            data.append(item)
        current_url = next_page(current_url, i + 1)

    assert data != []

    data = scalg.score_columns(data, [2, 3, 4], [0, 1, 0])

    if db:
        return data, database
    else:
        return data


# existing searches checker
def checker(data: list) -> list:
    changed = False
    car_urls = [d[0] for d in data]
    for link in car_urls:
        new_price = check_car_price(link)
        if not float(new_price) == float(data[car_urls.index(link)][2]):
            changed = True
            data[car_urls.index(link)][2] = new_price

    assert changed == True
    return data
