
from scraper import check_car_price
from scalg import score

# existing searches checker
def checker(data : list) -> list:

    car_urls = [d[0] for d in data if not d[0] in car_urls]
    for link in car_urls:
        new_price = check_car_price(link)
        if not new_price == data[data.index(link)][1]:
            data[data.index(link)][1] = new_price

    return data
