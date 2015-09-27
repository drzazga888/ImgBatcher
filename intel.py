import json
import os
from PIL import Image, ImageFilter

__author__ = 'drzazga888'


class Images:
    """ klasa przechowuje ścieżkę katalogu ze zdjęciami i nazwy obrazków
    """
    def __init__(self):
        self.items = []
        self.path = None

    def select_dir(self, path):
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp')):
                self.items.append((os.path.join(path, f)))


class Batcher:
    """ klasa bazowa dla modułów operujących na obrazkach
    """
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
    """ klasa, która zmienia nazwy obrazkom
    """
    def __init__(self, images):
        super().__init__(images)
        self.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/renamed'
        self.prop['text'] = 'obrazek_'
        self.prop['digits'] = 3
        self.prop['sort_by'] = 'name'

    def perform(self):
        pass
        # self.images.items =
        # for image in self.images.items:


class Resizer(Batcher):
    """ klasa tworzy miniatury
    """
    def __init__(self, images):
        super().__init__(images)
        self.prop['size'] = (256, 256)
        self.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/resized'
        self.prop['quality'] = 90
        self.prop['sharpen'] = True

    def perform(self):
        for image in self.images.items:
            image = Image.open(image)
            name = os.path.splitext(os.path.basename(image.filename))[0]
            if self.prop['sharpen']:
                image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=250, threshold=0))
            image.thumbnail(self.prop['size'])
            image.save(os.path.join(self.prop['destination'], name + '.jpg'), 'JPEG', quality=self.prop['quality'])
