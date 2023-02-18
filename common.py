import os
from easy_input import *

os.system("color")

# 获取文件名
def get_file_name(file_path):
    return file_path[
        max(file_path.rfind("/") + 1, file_path.rfind("\\") + 1) : file_path.rfind(".")
    ]


# 新建文件夹
def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


# 删除文件/文件夹
def remove_file_folder(path):
    if os.path.exists(path):
        os.remove(path)
