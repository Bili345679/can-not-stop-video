import random
import cv2
import os
import numpy as np

class BitImg:
    def __init__(
        self,
        height,
        width,
        empty_flag=False,
        fill_val="0",
        random_seed=False,
        load_flag=False,
        bit_list_str=False,
        file_name=False,
    ):
        self.height = height
        self.width = width
        self.bit_list_str_len = height * width
        self.random_seed = random_seed

        # 文件保存位置
        if not file_name:
            file_name = (
                str(height)
                + "_"
                + str(width)
                + "_"
                + (
                    ("E" + str(fill_val))
                    if empty_flag
                    else (
                        "R" + str(random_seed) if random_seed is not False else "random"
                    )
                )
            )

        self.bit_list_file_path = "./bit_list/%s.bin" % (file_name)
        self.bit_img_path = "./bit_img/%s.png" % (file_name)

        # bit 列表
        if bit_list_str:
            # 直接赋值
            self.bit_list_str = bit_list_str
        elif load_flag:
            # 读取bit_list文件
            self.load_bit_list()
        elif empty_flag:
            # 填充相同bit
            self.fill_bit_list(fill_val)
        else:
            # 随机bit
            self.random_bit_list_str()

    # 填充 bit 列表
    def fill_bit_list(self, fill_val="0"):
        self.bit_list_str = "".rjust(self.bit_list_str_len, fill_val)

    # 创建随机 bit 列表
    def random_bit_list_str(self):
        if self.random_seed is not False:
            random.seed(self.random_seed)

        bit_list_str_list = []
        temp_bit_list_str_len = 0
        while temp_bit_list_str_len <= self.bit_list_str_len:
            val = str(random.random())[2:]
            if "e" in val:
                val = val[: val.find("e")]
            bin_list_str = bin(int(val))[2:]
            bit_list_str_list.append(bin_list_str)
            temp_bit_list_str_len += len(bin_list_str)

        self.bit_list_str = "".join(bit_list_str_list)[0 : self.bit_list_str_len]

    # 向文件中保存bit信息
    def save_bit_list(self, force=False):
        if os.path.exists(self.bit_list_file_path):
            if force:
                # 删除
                os.remove(self.bit_list_file_path)
            else:
                return True

        # 字节缓存大小(4096倍数)
        bytes_cache_size = 4096
        # 缓存byte列表
        bytes_cache_list = []

        with open(self.bit_list_file_path + ".temp", "wb") as file:
            for each_byte_start in range(0, self.bit_list_str_len, 8):
                # bit 转byte
                cache_bit_list = self.bit_list_str[
                    each_byte_start : each_byte_start + 8
                ].ljust(8, "0")
                cache_byte_int = int(cache_bit_list, 2)
                bytes_cache_list.append(int(cache_byte_int))

                # bytes 缓存数量足够，写入文件
                if len(bytes_cache_list) == bytes_cache_size:
                    file.write(bytes(bytes_cache_list))
                    bytes_cache_list = []

            # 写入未写入的 bytes 缓存
            if len(bytes_cache_list):
                file.write(bytes(bytes_cache_list))

        # 重命名
        os.rename(self.bit_list_file_path + ".temp", self.bit_list_file_path)

    # 从文件中读取bit信息
    def load_bit_list(self):
        with open(self.bit_list_file_path, "rb") as file:
            bytes_list = file.read()

        bit_byte_list = [bin(byte)[2:].rjust(8, "0") for byte in bytes_list]
        self.bit_list_str = "".join(bit_byte_list)[: self.bit_list_str_len]

    # 预览图片
    def print_bit_list(self):
        for each_row_start in range(0, self.bit_list_str_len, self.width):
            for each_bit in self.bit_list_str[
                each_row_start : each_row_start + self.width
            ]:
                if each_bit == "0":
                    print("__|", end="")
                else:
                    print("##|", end="")
            print()

    # 保存图片
    def save_bit_img(self):
        bit_numpy = self.get_bit_numpy()

        cv2.imwrite(
            self.bit_img_path,
            bit_numpy,
            [cv2.IMWRITE_PNG_COMPRESSION, 0],
        )

    # 获取 numpy 格式
    def get_bit_numpy(self):
        bit_list = []
        for row_start in range(0, self.bit_list_str_len, self.width):
            bit_list.append(
                [
                    (255 if num == "0" else 1)
                    for num in list(
                        self.bit_list_str[row_start : row_start + self.width]
                    )
                ]
            )
        bit_numpy = np.asarray(bit_list, dtype="i2")
        return bit_numpy

