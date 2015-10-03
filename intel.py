import json
import os
import threading

from PIL import Image, ImageFilter

__author__ = 'drzazga888'


class Batcher(threading.Thread):
    """ klasa bazowa dla modułów operujących na obrazkach
    """

    extensions = ('jpg', 'jpeg', 'png', 'bmp')

    def __init__(self):
        super().__init__()
        self.path = ""
        self.names = []
        self.prop = {}
        self.processed = 0
        self.total = 0
        self.close_request = False

    def select_dir(self, path):
        self.names = []
        self.path = path
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(Batcher.extensions):
                self.names.append(f)
        self.total = len(self.names)

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
        for img_name in self.names:
            if self.close_request:
                self.close_request = False
                return
            self.process_single(img_name, self.processed)
            self.processed += 1
        self.processed = 0
        self.total = 0

    def process_single(self, img_name, img_nr):
        pass


class Renamer(Batcher):
    """ klasa, która zmienia nazwy obrazkom
    """

    temp_name = "_IMG_BATCHER_TEMP_"

    def __init__(self):
        super().__init__()
        self.transformation_schema = []
        self.transformation_schema_str = ""

    def create_transformation_schema(self):
        self.transformation_schema = []
        counter = 0
        for img_name in self.names:
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

    def process_single(self, img_name, img_nr):
        if os.path.isfile(self.transformation_schema[img_nr]['after']):
            os.rename(os.path.join(self.path, self.transformation_schema[img_nr]['before']),
                      os.path.join(self.path, self.temp_name))
            self.transformation_schema[img_nr]['before'] = self.temp_name
        os.rename(os.path.join(self.path, self.transformation_schema[img_nr]['before']),
                  os.path.join(self.path, self.transformation_schema[img_nr]['after']))


class Resizer(Batcher):
    """ klasa tworzy miniatury
    """

    def __init__(self):
        super().__init__()

    def process_single(self, img_name, img_nr):
        img = Image.open(os.path.join(self.path, img_name))
        img_name_root = os.path.splitext(img_name)[0]
        if self.prop['sharpen']:
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=0))
        img.thumbnail(self.prop['size'])
        img.save(os.path.join(self.prop['destination'], img_name_root + '.jpg'), 'JPEG',
                 quality=self.prop['quality'])

#TODO try catch na wybor folderu