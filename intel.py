from PyQt4 import QtCore
import json
import os
from PIL import Image
import math

__author__ = 'drzazga888'


class Batcher(QtCore.QThread):
    """ klasa bazowa dla modułów operujących na obrazkach
    """

    wait_time_ms = 50
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
        self.check_dir(path)
        self.path = path
        for f in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(Batcher.extensions):
                self.names.append(f)
        self.total = len(self.names)

    @staticmethod
    def check_dir(path):
        if path == "" or path is None:
            raise ValueError('Ścieżka katalogu źródłowego nie może być pusta')
        if not os.path.exists(path):
            raise ValueError('Katalog źródłowy nie istnieje')
        if not os.path.isdir(path):
            raise ValueError('Podana ścieżka katalogu źródłowego nie jest katalogiem')

    def load_prop(self, path):
        file = open(path, "r")
        prop_encoded = file.read()
        file.close()
        data_to_load = json.loads(prop_encoded)
        if data_to_load['name'] != self.__class__.__name__:
            raise NameError
        data_to_load.pop('name', None)
        self.prop = data_to_load

    def save_prop(self, path):
        file = open(path, "w")
        data_to_save = self.prop
        data_to_save['name'] = self.__class__.__name__
        prop_encoded = json.dumps(data_to_save)
        file.write(prop_encoded)
        file.close()

    def run(self):
        for img_name in self.names:
            if self.close_request:
                self.close_request = False
                return
            self.process_single(img_name, self.processed)
            self.processed += 1
        self.stop()

    def stop(self):
        if self.isRunning():
            self.close_request = True
        self.processed = 0
        self.total = 0

    def set_prop(self, name, value):
        self.prop[name] = value

    def process_single(self, img_name, img_nr):
        pass

    def validate_prop(self, name, value):
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

    def set_prop(self, name, value):
        if name == "text":
            value = str(value)
            if value == "" or value is None:
                raise ValueError('Tekst początkowy nie może być pusty')
            self.prop[name] = value
        elif name == "digits":
            if value == "":
                raise ValueError('Pole "ilość cyfr" musi być wypełnione')
            if not value.isdigit():
                raise ValueError('Ilość cyfr musi być liczbą całkowitą')
            value = int(value)
            if not 1 <= value <= 10:
                raise ValueError('Jakość musi być z przedziału od 1 do 10')
            self.prop[name] = value
        else:
            raise KeyError


class Resizer(Batcher):
    """ klasa tworzy miniatury
    """

    def __init__(self):
        super().__init__()

    def process_single(self, img_name, img_nr):
        img = Image.open(os.path.join(self.path, img_name))
        img_name_root = os.path.splitext(img_name)[0]
        covering_size = self._get_covering_size(img.size)
        img.thumbnail(covering_size, Image.ANTIALIAS)
        if covering_size != self.prop['size']:
            cropping_box = self._get_cropping_box(img.size)
            img = img.crop(cropping_box)
        img.save(os.path.join(self.prop['destination'], img_name_root + '.jpg'), 'JPEG',
                 quality=self.prop['quality'])

    def set_prop(self, name, value):
        if name == "destination":
            value = str(value)
            if value == "" or value is None:
                raise ValueError('Ścieżka katalogu docelowego nie może być pusta')
            if not os.path.exists(value):
                raise ValueError('Katalog docelowy nie istnieje')
            if not os.path.isdir(value):
                raise ValueError('Podana ścieżka katalogu docelowego nie jest katalogiem')
            self.prop[name] = value
        elif name == "size":
            if value[0] == "":
                raise ValueError('Pole "szerokość" musi być wypełnione')
            if value[1] == "":
                raise ValueError('Pole "wysokość" musi być wypełnione')
            if not value[0].isdigit():
                raise ValueError('Szerokość musi być liczbą całkowitą')
            if not value[1].isdigit():
                raise ValueError('Wysokość musi być liczbą całkowitą')
            value = (int(value[0]), int(value[1]))
            if not 1 <= value[0] <= 4000:
                raise ValueError('Szerokość musi być z przedziału od 1 do 4000')
            if not 1 <= value[1] <= 4000:
                raise ValueError('Wysokość musi być z przedziału od 1 do 4000')
            self.prop[name] = value
        elif name == "quality":
            if value == "":
                raise ValueError('Pole "jakość" musi być wypełnione')
            if not value.isdigit():
                raise ValueError('Jakość musi być liczbą całkowitą')
            value = int(value)
            if not 1 <= value <= 100:
                raise ValueError('Jakość musi być z przedziału od 1 do 100')
            self.prop[name] = value
        else:
            raise KeyError

    def _get_covering_size(self, img_size):
        asp_w_h = img_size[0] / img_size[1]
        w_h = self.prop['size']
        w = w_h[0]
        h = w_h[1]
        w_asp = int(math.ceil(h * asp_w_h))
        h_asp = int(math.ceil(w / asp_w_h))
        if w_asp > w:
            return w_asp, h
        else:
            return w, h_asp

    def _get_cropping_box(self, img_size):
        horizontal_pad = int((img_size[0] - self.prop['size'][0]) * 0.5)
        vertical_pad = int((img_size[1] - self.prop['size'][1]) * 0.5)
        return horizontal_pad, vertical_pad, img_size[0] - horizontal_pad, img_size[1] - vertical_pad


class Watermarker(Batcher):
    """ klasa tworzy znaki wodne
    """

    def __init__(self):
        super().__init__()
        self.watermark = None

    def run(self):
        self.watermark = Image.open(self.prop['watermark_source'])
        super().run()

    def process_single(self, img_name, img_nr):
        img = Image.open(os.path.join(self.path, img_name))
        img_name_root = os.path.splitext(img_name)[0]
        img.paste(self.watermark, box=self._get_pasting_box(img.size, self.watermark.size))
        img.save(os.path.join(self.prop['destination'], img_name_root + '.jpg'), 'JPEG',
                 quality=self.prop['quality'])

    def set_prop(self, name, value):
        if name == "pasting_corner" and value not in ['top-left', 'top-right', 'bottom-right', 'bottom-left']:
            raise ValueError("Zła wartość położenia znaku wodnego")
        if name in ["watermark_source", "destination", "pasting_corner"]:
            self.prop[name] = value
        elif name == "quality":
            self.prop[name] = int(value)
        else:
            raise KeyError

    def _get_pasting_box(self, img_size, watermark_size):
        if self.prop['pasting_corner'] == 'top-left':
            return 0, 0
        elif self.prop['pasting_corner'] == 'top-right':
            return 0, img_size[1] - watermark_size[1]
        elif self.prop['pasting_corner'] == 'bottom-right':
            return img_size[0] - watermark_size[0], img_size[1] - watermark_size[1]
        elif self.prop['pasting_corner'] == 'bottom-left':
            return img_size[0] - watermark_size[0], 0
