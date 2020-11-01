import json
from difflib import SequenceMatcher

# load makes and models from json file
def load_makes(website: str, _MAKES_JSON: str) -> dict:
    with open(_MAKES_JSON, "r", encoding="utf-8", newline="") as mjson:
        data = mjson.read()
        makes_dict = json.loads(data)
        makes_dict = makes_dict[website]
    return makes_dict


from settings import _MDE_MAKES_DICT, MATCH_RATIO


def table_name(title_data) -> str:
    if type(title_data) == list:
        return (
            '"'
            + title_data[0].replace(" ", "-")
            + "_"
            + title_data[1].replace(" ", "-")
            + '"'
        )
    elif "_" in title_data:
        return '"' + title_data + '"'


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
    return car_make, car_model, database


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

    og = [db_indexes[0], db_indexes[1]]
    database = ""
    if not og[0] == 0 or not og[0] == "":
        for make in _MDE_MAKES_DICT:
            if make["i"] == og[0]:
                database += str(make["n"]).replace(" ", "-") + "_"
                if not og[1] == 0 or not og[1] == "":
                    for model in make["models"]:
                        if model["v"] == og[1]:
                            database += str(model["m"]).replace(" ", "-")
                            break
                break

    return database
