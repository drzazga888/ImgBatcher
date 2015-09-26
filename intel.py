__author__ = 'drzazga888'

from PIL import Image


class Images:

    def __init__(self):
        self.items = []

    def add(self, image):
        pass

    def remove(self, image_id):
        pass


class Batcher:

    def __init__(self, images):
        self.images = images

    def load_prop(self):
        pass

    def perform(self):
        pass


class Renamer(Batcher):

    def perform(self):
        pass


class Resizer(Batcher):

    def perform(self):
        pass