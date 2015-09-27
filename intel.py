import json
import os

__author__ = 'drzazga888'

from PIL import Image


class Images:
    def __init__(self):
        self.items = []
        self.path = None

    def select_dir(self, path):
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp')):
                self.items.append(Image.open(os.path.join(path, f)))


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
        self.prop['renamer1'] = 'renamer2'

    def perform(self):
        pass


class Resizer(Batcher):
    def __init__(self, images):
        super().__init__(images)

    def perform(self):
        for image in self.images.items:
            name = os.path.basename(image.filename)
            image.thumbnail(self.prop['size'])
            image.save(os.path.join(self.prop['destination'], name), 'JPEG')
