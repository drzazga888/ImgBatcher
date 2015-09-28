from intel import *
import time

__author__ = 'drzazga888'

if __name__ == '__main__':

    # tworzenie miniatur
    print("---TWORZENIE MINIATUR---")
    batcher = Resizer()
    batcher.select_dir("/media/mario/Dokumenty/Zdjęcia/Moje prace")
    batcher.start()
    while batcher.isAlive():
        print("wykonano " + str(batcher.processed_images()) + " na " + str(batcher.total_images()))
        time.sleep(0.05)
    batcher.join()
    print("zakończono!")

    # zmiana nazw
    print("---ZMIANA NAZW---")
    batcher = Renamer()
    batcher.select_dir("/home/mario/PycharmProjects/ImgBatcher/resized")
    batcher.create_transformation_schema()
    print(batcher.transformation_schema_str)
    batcher.start()
    while batcher.isAlive():
        print("wykonano " + str(batcher.processed_images()) + " na " + str(batcher.total_images()))
        time.sleep(0.05)
    batcher.join()
    print("zakończono!")
