import json
import os
import threading

from PIL import Image, ImageFilter

__author__ = 'drzazga888'


class Images:
    """ klasa operuje na zbiorze obrazków
    """

    def __init__(self):
        self.names = []
        self.path = ""

    def select_dir(self, path):
        self.path = path
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp')):
                self.names.append(f)


class Batcher(threading.Thread):
    """ klasa bazowa dla modułów operujących na obrazkach
    """

    def __init__(self, images):
        super().__init__()
        self.images = images
        self.prop = {}
        self.processed = 0

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

    def run(self):
        for img_name in self.images.names:
            self.process_single(img_name)
            self.processed += 1

    def process_single(self, img_name):
        pass

    def processed_images(self):
        return self.processed

    def total_images(self):
        return len(self.images.items)


class Renamer(Batcher):
    """ klasa, która zmienia nazwy obrazkom
    """

    def __init__(self, images):
        super().__init__(images)
        self.transformation_schema = []
        self.transformation_schema_str = ""
        self.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/renamed'
        self.prop['text'] = 'obrazek_'
        self.prop['digits'] = 3

    def create_transformation_schema(self):
        self.transformation_schema = []
        counter = 0
        for img_name in self.images.names:
            self.transformation_schema.append({
                'before': img_name,
                'after': self.prop['text'] + ("{0:0=" + str(self.prop['digits']) + "d}").format(
                    counter) + os.path.splitext(img_name)[-1]
            })
            counter += 1
        self._create_transformation_schema_str()

    def _create_transformation_schema_str(self):
        self.transformation_schema_str = ""
        max_before_len = 0
        for single_transformation in self.transformation_schema:
            before_len = len(single_transformation['before'])
            if before_len > max_before_len:
                max_before_len = before_len
        for single_transformation in self.transformation_schema:
            self.transformation_schema_str += single_transformation['before'].ljust(max_before_len)
            self.transformation_schema_str += " --> "
            self.transformation_schema_str += single_transformation['after']
            self.transformation_schema_str += '\n'

    def process_single(self, img_name):
        pass


class Resizer(Batcher):
    """ klasa tworzy miniatury
    """

    def __init__(self, images):
        super().__init__(images)
        self.prop['size'] = (256, 256)
        self.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/resized'
        self.prop['quality'] = 90
        self.prop['sharpen'] = True

    def process_single(self, img_name):
        img = Image.open(os.path.join(img_name, self.images.path))
        img_name_root = os.path.splitext(img_name)[0]
        if self.prop['sharpen']:
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=0))
        img.thumbnail(self.prop['size'])
        img.save(os.path.join(self.prop['destination'], img_name_root + '.jpg'), 'JPEG',
                 quality=self.prop['quality'])
