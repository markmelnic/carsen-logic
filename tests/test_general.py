import os, json, unittest

from db import DB
from settings import *

# test utilities
class Utilities(unittest.TestCase):
    def test_makes_json(self):
        try:
            makes = load_makes("mobile_de")
        except json.decoder.JSONDecodeError:
            os.remove(_MAKES_JSON)
        except FileNotFoundError:
            self.skipTest("Makes json file not found.")
        self.assertIsNot(load_makes("mobile_de"), "" or None)


# database tests
class Database(unittest.TestCase):
    def test_db(self):
        db = DB()
        self.assertTrue(db)
        db.close_conn()
