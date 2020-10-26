import os, csv, unittest

from settings import *
from mobile_de.methods import *
from mobile_de.scraper import *

# test mobile_de methods
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
        data = surface_search(TEST_SEARCH_PARAMS)

        try:
            checker(data)
        except AssertionError:
            # no changes found
            pass


# test mobile_de scraper
class Scraper(unittest.TestCase):
    def test_search_url(self):
        url, pages_number = search_url(TEST_SEARCH_PARAMS, False)
        self.assertTrue(type(url) == str and url != "", url)
        self.assertTrue(pages_number > 0)
