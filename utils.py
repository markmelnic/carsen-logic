from json import loads
from requests import get
from bs4 import BeautifulSoup

# load makes and models from json file
def load_makes(website: str, _MAKES_JSON: str) -> dict:
    with open(_MAKES_JSON, "r", encoding="utf-8", newline="") as mjson:
        data = mjson.read()
        makes_dict = loads(data)
        makes_dict = makes_dict[website]
    return makes_dict


from difflib import SequenceMatcher
from settings import _MDE_MAKES_DICT, MATCH_RATIO, HEADERS

# generate db table name
def table_name(title_data) -> str:
    if type(title_data) == list:
        return (
            '"'
            + title_data[0].replace(" ", "-")
            + "_"
            + title_data[1].replace(" ", "-")
            + '"'
        )
    else:
        return '"' + title_data.replace(" ", "-") + '"'


# turn list into tuples
def tuplify(data: list) -> list:
    return [(d,) for d in data]


# match make and model for corresponding ids and db table
def make_model_matcher(car_make: str, car_model: str) -> list:
    og = [car_make, car_model]
    database = ""
    if not og[0].lower() == "any" or not og[0] == "":
        make_matcher = []
        for make in _MDE_MAKES_DICT:
            make_matcher.append(
                SequenceMatcher(a=make["n"].lower(), b=car_make).ratio()
            )
            if make["n"].lower() == og[0]:
                car_make = str(make["i"])
                database += str(make["n"]).replace(" ", "-") + "_"
                if not og[1] == "any" or not og[1] == "":
                    model_matcher = []
                    for model in make["models"]:
                        model_matcher.append(
                            SequenceMatcher(a=model["m"].lower(), b=car_model).ratio()
                        )
                        if model["m"].lower() == og[1]:
                            car_model = str(model["v"])
                            database += str(model["m"]).replace(" ", "-")
                            break
                    if car_model == og[1] and any(
                        x for x in model_matcher if x > MATCH_RATIO
                    ):
                        car_model = make["models"][
                            model_matcher.index(max(model_matcher))
                        ]
                        database = str(car_model["m"]).replace(" ", "-")
                        car_model = car_model["v"]
                break

        if car_make == og[0] and any(x for x in make_matcher if x > MATCH_RATIO):
            car_make = _MDE_MAKES_DICT[make_matcher.index(max(make_matcher))]
            database += str(car_make["n"]).replace(" ", "-") + "_"
            car_make = car_make["i"]
            model_matcher = []
            for model in _MDE_MAKES_DICT[make_matcher.index(max(make_matcher))][
                "models"
            ]:
                model_matcher.append(
                    SequenceMatcher(a=model["m"].lower(), b=car_model).ratio()
                )
                if model["m"].lower() == og[1]:
                    car_model = str(model["v"])
                    database = str(model["m"]).replace(" ", "-")
                    break
            if car_model == og[1] and any(x for x in model_matcher if x > MATCH_RATIO):
                car_model = _MDE_MAKES_DICT[make_matcher.index(max(make_matcher))][
                    "models"
                ][model_matcher.index(max(model_matcher))]
                database = str(car_model["m"]).replace(" ", "-")
                car_model = car_model["v"]
    return car_make, car_model, table_name(database)


# find make and model id from url and return table name
def index_db_finder(url: str) -> str:
    db_indexes = []
    # find url make id
    make_sub = "&makeModelVariant1.makeId="
    if make_sub in url:
        make_id = []
        for ch in url[url.find(make_sub) + len(make_sub) :]:
            try:
                int(ch)
                make_id.append(ch)
            except ValueError:
                db_indexes.append("".join(make_id))
                break
    # find url model id
    model_sub = "&makeModelVariant1.modelId="
    if model_sub in url:
        model_id = []
        for ch in url[url.find(model_sub) + len(model_sub) :]:
            try:
                int(ch)
                model_id.append(ch)
            except ValueError:
                db_indexes.append("".join(model_id))
                break

    return index_to_dbname(db_indexes[0], db_indexes[1])


def index_db_finder_js(url: str) -> str:
    response = get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    scripts = soup.find_all("script")
    for s in scripts:
        contents = s.get_text()
        if "setAdData({" in contents:
            make_id = ""
            make_id_text = "adSpecificsMakeId"
            for ch in contents[contents.find(make_id_text) + len(make_id_text) + 2 :]:
                if not ch == ",":
                    make_id += ch
                else:
                    break

            model_id = ""
            model_id_text = "adSpecificsModelId"
            for ch in contents[contents.find(model_id_text) + len(model_id_text) + 2 :]:
                if not ch == ",":
                    model_id += ch
                else:
                    break

            return index_to_dbname(make_id, model_id)


def index_to_dbname(make_id, model_id):
    database = ""
    if not make_id == 0 or not make_id == "":
        for make in _MDE_MAKES_DICT:
            if make["i"] == make_id:
                database += str(make["n"]).replace(" ", "-")
                if not model_id == 0 or not model_id == "":
                    for model in make["models"]:
                        if model["v"] == model_id:
                            database += "_" + str(model["m"]).replace(" ", "-")

    return table_name(database)
