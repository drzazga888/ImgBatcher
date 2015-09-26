import json
from os import listdir
from os.path import isfile, join

__author__ = 'drzazga888'

from PIL import Image


class Images:
    def __init__(self):
        self.items = []
        self.path = None

    def select_dir(self, path):
        for f in listdir(path):
            if isfile(join(path, f)) and f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp')):
                self.items.append(Image.open(join(path, f)))
        print(self.items)


class Batcher:
    def __init__(self, images):
        self.images = images
        self.prop = {}

    def load_prop(self, path):
        file = open(path, "r")
        prop_encoded = file.read()
        self.prop = json.loads(prop_encoded)
        file.close()

    def save_prop(self, path):
        file = open(path, "w")
        prop_encoded = json.dumps(self.prop)
        file.write(prop_encoded)
        file.close()

    def perform(self):
        pass


class Renamer(Batcher):
    def __init__(self, images):
        super().__init__(images)
        super().prop = {
            'renamer1': 'renamer2'
        }

    def perform(self):
        pass


class Resizer(Batcher):
    def __init__(self, images):
        super().__init__(images)
        super().prop = {
            'batcher1': 'batcher2'
        }

    def perform(self):
        pass
