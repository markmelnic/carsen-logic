# general settings
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

_MAKESJSON = "makes.json"

# database settings
CARS_DB = "db.sqlite3"
TABLE_DATA = [
    ("url", "TEXT"),
    ("title", "TEXT"),
    ("price", "REAL"),
    ("registration", "REAL"),
    ("mileage", "REAL"),
    ("type", "TEXT"),
    ("fuel", "TEXT"),
    ("transmission", "TEXT"),
    ("color", "TEXT"),
    ("options", "TEXT"),
    ("score", "REAL"),
]


# test settings
TEST_MAKESJSON = "tests/test_data/makes_test_copy.json"
TEST_DATA_FILE = "tests/test_data/data.csv"
TEST_SEARCH_PARAMS = ["Lexus", "LC 500h", "", "", "", "", "", ""]
