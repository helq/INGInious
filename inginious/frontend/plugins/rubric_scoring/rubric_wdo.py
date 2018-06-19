import json
from pprint import pprint


class RubricWdo():

    def __init__(self, source):
        self.data = self.read_data(source)


    def read_data(self, source):
        with open(source) as f:
            data = json.load(f)
            pprint(data)
            return data