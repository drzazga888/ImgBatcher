from intel import *
import time

__author__ = 'drzazga888'

if __name__ == '__main__':

    # wybieranie folderu
    i = Images()
    i.select_dir("/media/mario/Dokumenty/Zdjęcia/Moje prace")

    # tworzenie miniatur
    print("---TWORZENIE MINIATUR---")
    r = Resizer(i)
    r.start()
    while r.isAlive():
        print("wykonano " + str(r.processed_images()) + " na " + str(r.total_images()))
        time.sleep(0.05)
    r.join()
    print("zakończono!")

    # wybieranie folderu
    i.select_dir("/home/mario/PycharmProjects/ImgBatcher/resized")

    # zmiana nazw
    print("---ZMIANA NAZW---")
    r = Renamer(i)
    r.create_transformation_schema()
    print(r.transformation_schema_str)
    r.start()
    while r.isAlive():
        print("wykonano " + str(r.processed_images()) + " na " + str(r.total_images()))
        time.sleep(0.05)
    r.join()
    print("zakończono!")
