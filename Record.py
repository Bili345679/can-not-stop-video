import json
import os
import random
from common import *
from Video import Video


class Record:
    def __init__(self):
        self.record_list_file_path = "./record_list.json"
        self.load_record_list()

        if self.has_unover_record():
            self.select_unover_record()
        else:
            self.input_new_record()

    # 从文件中读取记录列表
    def load_record_list(self):
        if not os.path.exists(self.record_list_file_path):
            with open(self.record_list_file_path, "w") as file:
                json.dump([], file)
            self.record_list = []
            return self.record_list

        with open(self.record_list_file_path, "r") as file:
            self.record_list = json.load(file)
            return self.record_list

    # 保存记录到列表中
    def save_record_list(self):
        with open(self.record_list_file_path, "w") as file:
            if not hasattr(self, "record_list"):
                json.dump([], file)
            else:
                json.dump(self.record_list, file)

    # 是否有未完成的记录
    def has_unover_record(self):
        unover_flag = False
        for each_record in self.record_list:
            if each_record["over"] == False:
                unover_flag = True
                break
        return unover_flag

    # 获取未完成的记录
    def get_unover_record(self):
        unover_record_list = []
        index = 0
        for each_record in self.record_list:
            if each_record["over"] == False:
                record = {"index": index, "video_path": each_record["video_path"]}
                unover_record_list.append(record)
            index += 1

        return unover_record_list

    # 用户输入新的记录
    def input_new_record(self):
        record = {}

        record["video_path"] = ezinput("输入视频地址：", default="", not_empty_flag=True)

        record["up_down_val"] = ezinput("上下层亮度区分值(0-255)", "int", 128)

        record["up_img_seed"] = ezinput("上层雪花图随机种子：", "int", False)
        if record["up_img_seed"] == False:
            record["up_img_seed"] = random.randint(0, 1000000)
        record["down_img_seed"] = ezinput("下层雪花图随机种子：", "int", False)
        if record["down_img_seed"] == False:
            record["down_img_seed"] = random.randint(0, 1000000)

        record["up_img_move_x"] = ezinput("上层雪花图 x 轴移动方向：", "int", 5)
        record["up_img_move_y"] = ezinput("上层雪花图 y 轴移动方向：", "int", 0)

        record["down_img_move_x"] = ezinput("下层雪花图 x 轴移动方向：", "int", -5)
        record["down_img_move_y"] = ezinput("下层雪花图 y 轴移动方向：", "int", 0)

        record["start_frame"] = ezinput("渲染开始帧", "int", 0)
        video = Video(record["video_path"])
        record["end_frame"] = ezinput("渲染结束帧", int, video.frame_total)

        record["process_total"] = ezinput("进程数", "int", 1)

        record["over"] = False

        self.record_list.append(record)

        self.record_index = len(self.record_list) - 1

        self.save_record_list()

        return self.get_now_record()

    # 选择未完成的记录
    def select_unover_record(self):
        ezprint("选择未完成的记录")
        unover_record = self.get_unover_record()
        index = 1
        for each_unover_record in unover_record:
            print("\t" + str(index) + "\t" + each_unover_record["video_path"])
            index += 1
        print("\tN\t新建记录")

        select = ezinput("选择记录", "int", "N")
        print(select)
        if select == "N":
            return self.input_new_record()
        else:
            select -= 1
            if not select in range(0, len(unover_record)):
                return self.select_unover_record()
            else:
                self.record_index = unover_record[select]["index"]
                return self.get_now_record()

    # 获取当前记录
    def get_now_record(self):
        return self.record_list[self.record_index]

    # 设置当前记录
    def set_now_record(self, key, value):
        self.record_index[self.record_index][key] = value
