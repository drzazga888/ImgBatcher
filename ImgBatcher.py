from intel import *

__author__ = 'drzazga888'

if __name__ == '__main__':
    i = Images()
    i.select_dir("/media/mario/Dokumenty/Zdjęcia/Moje prace")
    r = Resizer(i)
    r.perform()
    r.prop['sharpen'] = False
    r.prop['destination'] = '/home/mario/PycharmProjects/ImgBatcher/resized_nosh'
    r.perform()