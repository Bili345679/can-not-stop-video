import time
from termcolor import colored

# print模式对应颜色
def mode_to_color(mode="info"):
    if not mode:
        return "white"

    mode_to_color_dict = {"info": "green", "warning": "yellow", "error": "red"}
    color_list = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    if mode in mode_to_color_dict:
        return mode_to_color_dict[mode]
    elif mode in color_list:
        return mode
    else:
        return "white"


# 带时间打印
def ezprint(val, mode="info", show_time=True):
    if show_time:
        print(add_data_time_head(str(val), mode))
    else:
        print(colored(val, mode_to_color(mode)))
    return val


# 带格式检测的输入
#   type 输入内容的格式
#   default 默认值
#   not_empty_flag 禁止为空(如果有默认值时，返回默认值)
#   mode 输出颜色 ["info","warning","error", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
#   show_time 展示时间
#   show_val 展示输入值
def ezinput(
    org_key,
    type="str",
    default="",
    not_empty_flag=False,
    mode="info",
    show_time=True,
    show_val=True,
):
    try:
        key = org_key
        if default != "":
            key += " (默认值%s)" % (str(default))

        if show_time:
            key = add_data_time_head(key, mode)
        else:
            key = colored(key, mode_to_color(mode))

        str_val = input(key)

        # 无输入
        if str_val == "":
            if default != "":
                str_val = default
                val = default
            elif not_empty_flag:
                ezprint("该值不能为空", "error")
                return ezinput(org_key, type, default, not_empty_flag, mode)
            else:
                str_val = default
                val = default
        elif type == "int":
            val = int(str_val)
        elif type == "float":
            val = float(str_val)
        else:
            val = str_val
    except Exception:
        return ezinput(org_key, type, default, not_empty_flag, mode)

    if show_val:
        ezprint("\t" + str(str_val), mode, show_time)
    return val


# 给字符串添加时间前缀
def add_data_time_head(str, mode=False, timestamp=False):
    return (
        colored("[" + get_data_time(timestamp) + "]", mode_to_color(mode)) + " " + str
    )


# 获取格式化时间
def get_data_time(timestamp=False):
    if not timestamp:
        timestamp = time.time()
    timestamp = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d_%H-%M-%S", timestamp)
