import json

from settings import _MAKESJSON, TEST_MAKESJSON

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


def table_name(s1: str, s2: str) -> str:
    return '"' + s1.replace(" ", "-") + "_" + s2.replace(" ", "-") + '"'
