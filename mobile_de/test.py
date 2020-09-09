
import json

_MAKESJSON = 'makes.json'

TEST_SEARCH = ['Lexus', 'IS300', '', '', '', '', '', '']

if __name__ == '__main__':
    from search import search
    
    print(search(TEST_SEARCH))

def load_makes(site : str) -> dict:
    with open(_MAKESJSON, 'r', encoding="utf-8", newline='') as mjson:
        data = mjson.read()
        makes_dict = (json.loads(data))
        makes_dict = makes_dict[site]
        mjson.close()
    return makes_dict
