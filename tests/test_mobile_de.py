import os, csv, json, unittest

from db import DB
from settings import *
from mobile_de.methods import *
from mobile_de.scraper import *


# tests for mobile_de methods
class Methods(unittest.TestCase):
    def test_search(self):
        data = search(TEST_SEARCH_PARAMS, db=False)
        self.assertIsNot(data, [] or None)
        self.assertTrue(type(data) == list)

    def test_surface_search(self):
        data = surface_search(TEST_SEARCH_PARAMS, db=False)
        self.assertIsNot(data, [] or None)
        self.assertTrue(type(data) == list)

    def test_checker(self):
        with open(TEST_DATA_FILE, "r") as csvfile:
            data = list(csv.reader(csvfile))

        try:
            checker(data)
        except AssertionError:
            # no changes found
            pass

    def test_makesjson(self):
        try:
            makes = load_makes("mobile_de")
        except json.decoder.JSONDecodeError:
            os.remove(_MAKES_JSON)
        except FileNotFoundError:
            self.skipTest("Makes json file not found.")
        self.assertIsNot(load_makes("mobile_de"), "" or None)


# tests for mobile_de scraper
class Scraper(unittest.TestCase):
    def test_search_url(self):
        url, pages_number = search_url(TEST_SEARCH_PARAMS, db=False)
        self.assertTrue(type(url) == str and url != "", url)
        self.assertTrue(pages_number > 0)


# test the database
class Database(unittest.TestCase):
    def test_db(self):
        db = DB()
        self.assertTrue(db)
        db.close_conn()
