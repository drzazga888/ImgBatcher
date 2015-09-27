from intel import *
import time

__author__ = 'drzazga888'

if __name__ == '__main__':
    i = Images()
    i.select_dir("/media/mario/Dokumenty/Zdjęcia/Moje prace")
    r = Resizer(i)
    r.start()
    while r.isAlive():
        print("wykonano " + str(r.processed_images()) + " na " + str(r.total_images()))
        time.sleep(0.05)
    r.join()
    print("zakończono!")