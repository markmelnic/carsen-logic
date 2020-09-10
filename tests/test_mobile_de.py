
import os, json

from settings import _MAKESJSON

# tests for mobile_de
from mobile_de.methods import *
class CheckMethods:
    def __init__(self):
        self.test_makesjson()

    def test_makesjson(self):
        try:
            load_makes('mobile_de')
        except json.decoder.JSONDecodeError:
            os.remove(_MAKESJSON)
        except FileNotFoundError:
            pass
