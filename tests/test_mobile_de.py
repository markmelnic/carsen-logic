import unittest
import os, csv, json
from settings import *

from mobile_de.methods import *


class Methods(unittest.TestCase):
    def test_search(self):
        data = search(TEST_SEARCH_PARAMS)
        self.assertIsNot(data, [] or None)
        self.assertTrue(type(data) == list)

    def test_surface_search(self):
        data = surface_search(TEST_SEARCH_PARAMS)
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
            os.remove(_MAKESJSON)
        except FileNotFoundError:
            self.skipTest("Makes json file not found.")
        self.assertIsNot(load_makes("mobile_de"), "" or None)


# tests mobile_de scraper
from mobile_de.scraper import *


class Scraper(unittest.TestCase):
    def test_search_url(self):
        makes = load_makes("mobile_de")
        url, pages_number = search_url(makes, TEST_SEARCH_PARAMS)
        self.assertTrue(type(url) == str and url != "", url)
        self.assertTrue(pages_number > 0)
