import os, json, unittest

from database import DB
from settings import *

# test utilities
class Utilities(unittest.TestCase):
    def test_makes_json(self):
        try:
            from settings import _MDE_MAKES_DICT
            self.assertIsNot(_MDE_MAKES_DICT, "" or None)
        except json.decoder.JSONDecodeError:
            pass
            # os.remove(_MAKES_JSON)
        except FileNotFoundError:
            self.skipTest("Makes json file not found.")


# database tests
class Database(unittest.TestCase):
    def test_db(self):
        db = DB()
        self.assertTrue(db)
        db.close_conn()
