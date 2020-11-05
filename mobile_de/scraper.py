from datetime import datetime
from requests import get
from bs4 import BeautifulSoup

from utils import make_model_matcher, index_db_finder, index_db_finder_js
from settings import (
    HEADERS,
    BASE_URL,
    REG_KEYS,
    PRICE_KEYS,
)


def search_url(inp: list, db: bool) -> list:
    # what each makes index is
    # 0 - make
    # 1 - model
    # 2 - minprice
    # 3 - maxprice
    # 4 - minreg
    # 5 - maxreg
    # 6 - minmileage
    # 7 - maxmileage

    # generate url parameters
    url_params = ""

    # handle make, model and database name
    car_make, car_model, database = make_model_matcher(inp[0].lower(), inp[1].lower())

    if car_model != "" or car_model != 0:
        url_params += "&makeModelVariant1.makeId=" + car_make
        url_params += "&makeModelVariant1.modelId=" + car_model
    else:
        # model
        if not inp[1].lower() == "any" or not inp[1] == "":
            url_params += "&makeModelVariant1.modelDescription=" + str(inp[1])

    # price
    if not inp[2] == "" or not inp[2] == 0:
        url_params += "&minPrice=" + str(inp[2])
    if not inp[3] == "" or not inp[3] == 0:
        url_params += "&maxPrice=" + str(inp[3])

    # registration
    if not inp[4] == "" or not inp[4] == 0:
        url_params += "&minFirstRegistrationDate=" + str(inp[4])
    if not inp[5] == "" or not inp[5] == 0:
        url_params += "&maxFirstRegistrationDate=" + str(inp[5])

    # mileage
    if not inp[6] == "" or not inp[6] == 0:
        url_params += "&minMileage=" + str(inp[6])
    if not inp[7] == "" or not inp[7] == 0:
        url_params += "&maxMileage=" + str(inp[7])

    url = BASE_URL + url_params + "&pageNumber=1&lang=en"

    # check number of pages
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    checker = soup.find(class_="h2 u-text-orange rbt-result-list-headline").get_text()
    checker = int(checker.split(" ")[0].replace(" ", "").replace(",", ""))

    pagesnr = soup.find_all(class_="btn btn--muted btn--s")
    if len(pagesnr) == 0:
        pagesnr = 1
    else:
        pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

    if db:
        return url, pagesnr, database
    else:
        return url, pagesnr


def next_page(current_url: str, current_page: int) -> str:
    if current_page < 10:
        return current_url[:-1] + str(current_page + 1)
    elif current_page >= 10:
        return current_url[:-2] + str(current_page + 1)


def surface_data(url: str) -> list:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    listings = soup.find_all(
        "a", {"class": "link--muted no--text--decoration result-item"}
    )

    data = []
    for listing in listings:
        listing_url = listing["href"]
        title = listing.find(class_="h3 u-text-break-word").get_text()
        price = int(
            listing.find(class_="h3 u-block")
            .get_text()
            .replace("\xa0", "")
            .replace(",", "")
            .replace(".", "")
            .replace("€", "")
        )

        # handle mileage and registration
        regmil = listing.find(class_="rbt-regMilPow").get_text().split(",")
        reg = regmil[0]
        if any(keyword in reg for keyword in REG_KEYS):
            reg = datetime.now().year
        else:
            reg = int(reg[-4:])
        try:
            mileage = int(regmil[1].replace(u"\xa0", "").replace(".", "")[:-2])
        except ValueError:
            mileage = 0

        data.append([listing_url, title, price, reg, mileage])

    return data


def get_page_listings(url: str) -> list:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    return [
        link["href"]
        for link in soup.find_all(
            "a", {"class": "link--muted no--text--decoration result-item"}
        )
    ]


def get_data(url: str, find_db=False) -> list:
    # check type of vehicle
    if url.find("scopeId=C") != -1:
        data = get_car_data(url)
    elif url.find("scopeId=MB") != -1:
        return #motorbike
    elif url.find("scopeId=MH") != -1:
        return #motor home and caravan
    else:
        return

    if find_db:
        try:
            database = index_db_finder(url)
        except IndexError:
            database = index_db_finder_js(url)
        finally:
            return data, database
    else:
        return data


def get_car_data(url: str, find_db=False) -> list:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # title
    car_title = soup.find(id="rbt-ad-title").get_text()

    # price
    car_price = soup.find(class_="h3 rbt-prime-price").get_text().replace(",", "")
    if any(keyword in car_price for keyword in PRICE_KEYS):
        car_price = int(car_price[1:-8])
    else:
        car_price = int(car_price[1:])

    # registration
    try:
        car_reg = soup.find(id="rbt-firstRegistration-v").get_text()
    except AttributeError:
        car_reg = soup.find(id="rbt-category-v").get_text()
    if any(keyword in car_reg for keyword in REG_KEYS):
        car_reg = datetime.now().year
    else:
        car_reg = int(car_reg[3:])

    # mileage
    car_mileage = soup.find(id="rbt-mileage-v").get_text().replace(".", "")[:-3]

    # power
    try:
        car_power = soup.find(id="rbt-power-v").get_text().split("(")[1][:-4]
    except AttributeError:
        car_power = 0

    # vehicle type
    car_type = soup.find(id="rbt-category-v").get_text().split(",")[0]

    # location
    location = soup.find(id="rbt-seller-address").get_text().replace("\xa0", " ")

    # fuel type
    try:
        fuel_type = soup.find(id="rbt-fuel-v").get_text()
    except AttributeError:
        fuel_type = ""

    # transmission
    try:
        transmission = soup.find(id="rbt-transmission-v").get_text().split(" ")[0]
    except AttributeError:
        transmission = ""

    # car color
    try:
        color = soup.find(id="rbt-color-v").get_text()
    except AttributeError:
        color = ""

    # options
    try:
        options = [
            option.get_text()
            for option in soup.find(id="rbt-features").find(class_="g-row")
        ]
    except AttributeError:
        options = []

    data = [
        url,
        car_title,
        int(car_price),
        int(car_reg),
        int(car_mileage),
        # int(car_power),
        car_type,
        location,
        fuel_type,
        transmission,
        # color,
        "|".join(options),
    ]


def check_car_price(url: str) -> int:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        car_price = soup.find(class_="h3 rbt-prime-price").get_text().replace(".", "")
    except AttributeError:
        return False

    car_price = soup.find(class_="h3 rbt-prime-price").get_text().replace(",", "")
    if any(keyword in car_price for keyword in PRICE_KEYS):
        return int(car_price[1:-8])
    else:
        return int(car_price[1:])
