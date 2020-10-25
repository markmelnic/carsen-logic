import json

_MAKES_JSON = "makes.json"
TEST_MAKESJSON = "tests/test_data/makes_test_copy.json"

# load makes and models from json file
def load_makes(website: str) -> dict:
    try:
        with open(_MAKES_JSON, "r", encoding="utf-8", newline="") as mjson:
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
