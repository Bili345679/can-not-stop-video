import time
from multiprocessing import Process
from Video import Video
from BitImg import BitImg
from FrameRender import FrameRender
from common import *

if __name__ == "__main__":
    # 初始化工作路径
    mk_dir("./bit_img")
    mk_dir("./bit_list")
    mk_dir("./bit_list")
    mk_dir("./org_video")
    mk_dir("./over_video")
    mk_dir("./rendered_frame")

    start_time = time.time()

    video_path = ezinput("输入视频地址：", default="", not_empty_flag=True)
    
    up_down_val = ezinput("上下层亮度区分值(0-255)", "int", 128)

    up_img_seed = ezinput("上层雪花图随机种子：", "int", False)
    down_img_seed = ezinput("下层雪花图随机种子：", "int", False)

    up_img_move_x = ezinput("上层雪花图 x 轴移动方向：", "int", 5)
    up_img_move_y = ezinput("上层雪花图 y 轴移动方向：", "int", 0)

    down_img_move_x = ezinput("下层雪花图 x 轴移动方向：", "int", -5)
    down_img_move_y = ezinput("下层雪花图 y 轴移动方向：", "int", 0)

    process_total = ezinput("进程数", "int", 1)

    # video_path = "./org_video/SaySo.flv"
    # video_path = "./org_video/test.mp4"
    # video_path = "./org_video/BadApple.mp4"
    # up_down_val = 172
    # up_img_seed = 1
    # down_img_seed = 2
    # up_img_move_x = 5
    # up_img_move_y = 0
    # down_img_move_x = -5
    # down_img_move_y = 0
    # process_total = 10

    # 视频模块
    video = Video(video_path)

    # 上层雪花图
    up_bit_img = BitImg(video.frame_height, video.frame_width, random_seed=up_img_seed)
    up_bit_list_str = up_bit_img.bit_list_str
    # 下层雪花图
    down_bit_img = BitImg(
        video.frame_height, video.frame_width, random_seed=down_img_seed
    )
    down_bit_list_str = down_bit_img.bit_list_str

    # 帧渲染进程
    frame_render = FrameRender(
        video_path,
        up_down_val,
        up_bit_list_str,
        down_bit_list_str,
        up_img_move_x,
        up_img_move_y,
        down_img_move_x,
        down_img_move_y,
    )

    # 每个进程负责的帧
    frame_render_process_work_list = []
    # 渲染进程列表
    frame_render_process_list = []
    for process_index in range(process_total):
        frame_render_process_work_list.append(
            range(process_index, video.frame_total, process_total)
        )

    for process_index in range(process_total):
        frame_render_process_list.append(
            Process(
                target=frame_render.render_frame,
                args=(
                    frame_render_process_work_list[process_index],
                    process_index,
                ),
            )
        )

    for each_process in frame_render_process_list:
        each_process.start()
        pass

    for each_process in frame_render_process_list:
        each_process.join()
        pass

    # 合成视频
    video.render_video()
    # 删除帧
    video.remove_render_frame()

    print(time.time() - start_time)
