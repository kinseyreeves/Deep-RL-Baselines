import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_size_map(size):
    return dir_path + f"/map_{size}x{size}.txt"

def get_3x3_map():
    return dir_path + "/map_3x3.txt"

def get_4x4_map():
    return dir_path + "/map_4x4.txt"


def get_5x5_map():
    return dir_path + "/map_5x5.txt"


def get_6x6_map():
    return dir_path + "/map_6x6.txt"


def get_7x7_map():
    return dir_path + "/map_7x7.txt"


def get_8x8_map():
    return dir_path + "/map_8x8.txt"


def get_empty_3x3_map():
    return dir_path + "/map_3x3_empty.txt"
