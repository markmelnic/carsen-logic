from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

from settings import HEADERS

BASE_URL = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"


def search_url(makes, inp: list) -> list:
    # what each makes index is
    inp[0] = inp[0].lower()  # 0 - make
    inp[1] = inp[1].lower()  # 1 - model
    # 2 - minprice
    # 3 - maxprice
    # 4 - minreg
    # 5 - maxreg
    # 6 - minmileage
    # 7 - maxmileage

    url_params = ""

    # handle make and model
    car_make = inp[0]
    car_model = inp[1]
    if not inp[0].lower() == "any" or not inp[0] == "":
        make_matcher = []
        for make in makes:
            make_matcher.append(
                SequenceMatcher(a=make["n"].lower(), b=car_make).ratio()
            )
            if make["n"].lower() == inp[0]:
                car_make = str(make["i"])
                if not inp[1] == "any" or not inp[1] == "":
                    model_matcher = []
                    for model in make["models"]:
                        model_matcher.append(
                            SequenceMatcher(a=model["m"].lower(), b=car_model).ratio()
                        )
                        if model["m"].lower() == inp[1]:
                            car_model = str(model["v"])
                            break
                    if car_model == inp[1] and any(x > 0.6 for x in model_matcher):
                        car_model = make["models"][
                            model_matcher.index(max(model_matcher))
                        ]["v"]
                break

        if car_make == inp[0] and any(x > 0.6 for x in make_matcher):
            car_make = makes[make_matcher.index(max(make_matcher))]["i"]
            model_matcher = []
            for model in makes[make_matcher.index(max(make_matcher))]["models"]:
                model_matcher.append(
                    SequenceMatcher(a=model["m"].lower(), b=car_model).ratio()
                )
                if model["m"].lower() == inp[1]:
                    car_model = str(model["v"])
                    break
            if car_model == inp[1] and any(x > 0.6 for x in model_matcher):
                car_model = makes[make_matcher.index(max(make_matcher))]["models"][
                    model_matcher.index(max(model_matcher))
                ]["v"]

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

    url = BASE_URL + url_params + "&pageNumber=1"

    # check number of pages
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    checker = soup.find(class_="h2 u-text-orange rbt-result-list-headline").get_text()
    checker = int(checker.split(" ")[0].replace(" ", "").replace(".", ""))

    pagesnr = soup.find_all(class_="btn btn--muted btn--s")
    if len(pagesnr) == 0:
        pagesnr = 1
    else:
        pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

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
        url = listing["href"]
        title = listing.find(class_ = "h3 u-text-break-word").get_text()
        price = listing.find(class_ = "h3 u-block").get_text().replace(u'\xa0', ' ').replace('.', '')[:-2]

        # handle mileage and registration
        regmil = listing.find(class_ = "rbt-regMilPow").get_text().split(",")
        reg = regmil[0]
        if "Neuwagen" in reg or "Tageszulassung" in reg:
            reg = datetime.now().year
        else:
            reg = reg[-4:]
        mileage = regmil[1].replace(u'\xa0', ' ').replace('.', '')[:-2].replace(' ', '')

        data.append([url, title, reg, price, mileage])

    return data


def get_car_links(url: str) -> list:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    return [
        link["href"]
        for link in soup.find_all(
            "a", {"class": "link--muted no--text--decoration result-item"}
        )
    ]


def get_car_data(url: str) -> list:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # title
    car_title = soup.find(id="rbt-ad-title").get_text()

    # price
    car_price = soup.find(class_="h3 rbt-prime-price").get_text().replace(".", "")
    if "Brutto" in car_price:
        car_price = int(car_price[:-11])
    else:
        car_price = int(car_price[:-2])

    # registration
    try:
        car_reg = soup.find(id="rbt-firstRegistration-v").get_text()
    except AttributeError:
        car_reg = soup.find(id="rbt-category-v").get_text()
    if "Neufahrzeug" in car_reg:
        car_reg = datetime.now().year

    # elif 'Vorführfahrzeug' in car_reg:
    #    car_reg = 4
    #    #carReg = 'Demo Car'
    # elif 'Jahreswagen' in car_reg:
    #    car_reg = 3
    #    #carReg = 'Employee Car'
    #    #Jahreswagen - employee car
    else:
        car_reg = int(car_reg[3:])

    # mileage
    car_mileage = soup.find(id="rbt-mileage-v").get_text().replace(".", "")[:-3]

    # power
    # car_power = soup.find(id = "rbt-power-v").get_text().split("(")[1][ : -4]

    return [url, car_title, car_reg, car_price, car_mileage]  # , car_power


def check_car_price(url: str) -> int:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        car_price = soup.find(class_="h3 rbt-prime-price").get_text().replace(".", "")
    except AttributeError:
        return False

    if "Brutto" in car_price:
        return int(car_price[:-11])
    else:
        return int(car_price[:-2])
