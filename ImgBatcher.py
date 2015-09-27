from intel import *

__author__ = 'drzazga888'

if __name__ == '__main__':
    i = Images()
    i.select_dir("/media/mario/Dokumenty/Zdjęcia/Moje prace")
    r = Resizer(i)
    r.prop['size'] = (128, 128)
    r.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/resized'
    r.perform()