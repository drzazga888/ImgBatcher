import json
import os
from PIL import Image, ImageFilter

__author__ = 'drzazga888'


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

    def perform(self):
        pass


class Resizer(Batcher):
    def __init__(self, images):
        super().__init__(images)
        self.prop['size'] = (256, 256)
        self.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/resized'
        self.prop['quality'] = 90
        self.prop['sharpen'] = True

    def perform(self):
        for image in self.images.items:
            name = os.path.splitext(os.path.basename(image.filename))[0]
            if self.prop['sharpen']:
                image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=250, threshold=0))
            image.thumbnail(self.prop['size'])
            image.save(os.path.join(self.prop['destination'], name + '.jpg'), 'JPEG', quality=self.prop['quality'])
