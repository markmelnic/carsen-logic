from utils import load_makes

# general settings
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

MATCH_RATIO = 0.6

_MAKES_JSON = "makes.json"
_MDE_MAKES_DICT = load_makes("mobile_de", _MAKES_JSON)

BASE_URL = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"
PRICE_KEYS = ["Gross"]
REG_KEYS = ["New vehicle", "New car", "Pre-Registration"]

# database settings
DB_NAME = "db.sqlite3"
CAR_TABLE_DATA = [
    ("url", "TEXT"),
    ("title", "TEXT"),
    ("price", "REAL"),
    ("registration", "REAL"),
    ("mileage", "REAL"),
    # ("power", "REAL"),
    ("type", "TEXT"),
    ("location", "TEXT"),
    ("fuel", "TEXT"),
    ("transmission", "TEXT"),
    # ("color", "TEXT"),
    ("options", "TEXT"),
    ("score", "REAL"),
]

# test settings
TEST_SEARCH_PARAMS = ["Lexus", "LC 500h", "", "", "", "", "", ""]
