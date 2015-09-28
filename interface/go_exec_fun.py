from intel import *
import time


def change_names(source_folder_name, name_list):
    print(source_folder_name, name_list)
    """batcher = Renamer()
    batcher.select_dir(source_folder_name)
    batcher.create_transformation_schema()
    print(batcher.transformation_schema_str)
    batcher.start()
    while batcher.isAlive():
        print("wykonano " + str(batcher.processed_images()) + " na " + str(batcher.total_images()))
        time.sleep(0.05)
    batcher.join()"""
    return True
    # return False  # na blad


def change_miniature_size(width, height, quality, source_folder_name, dest_folder_name, is_sharpen):
    print(width, height, quality, source_folder_name, dest_folder_name, is_sharpen)
    batcher = Resizer()
    batcher.select_dir(source_folder_name)
    batcher.prop['size'] = (width, height)
    batcher.prop['destination'] = dest_folder_name
    batcher.prop['quality'] = quality
    batcher.prop['sharpen'] = is_sharpen
    batcher.start()
    while batcher.isAlive():
        print("wykonano " + str(batcher.processed_images()) + " na " + str(batcher.total_images()))
        time.sleep(0.05)
    batcher.join()
    return True
    # return False  # na blad
