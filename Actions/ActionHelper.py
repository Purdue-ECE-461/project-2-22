import os


def check_file(path):
    return os.path.exists(path)


def check_folder_path(folder_path):
    return os.path.isdir(folder_path)