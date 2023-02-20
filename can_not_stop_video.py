import time
from multiprocessing import Process
from Record import Record
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

    record = Record()
    now_record = record.get_now_record()

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

    start_time = time.time()

    # 视频模块
    video = Video(now_record["video_path"])

    # 上层雪花图
    up_bit_img = BitImg(
        video.frame_height, video.frame_width, random_seed=now_record["up_img_seed"]
    )
    up_bit_list_str = up_bit_img.bit_list_str
    # 下层雪花图
    down_bit_img = BitImg(
        video.frame_height, video.frame_width, random_seed=now_record["down_img_seed"]
    )
    down_bit_list_str = down_bit_img.bit_list_str

    # 帧渲染进程
    frame_render = FrameRender(
        now_record["video_path"],
        now_record["up_down_val"],
        up_bit_list_str,
        down_bit_list_str,
        now_record["up_img_move_x"],
        now_record["up_img_move_y"],
        now_record["down_img_move_x"],
        now_record["down_img_move_y"],
    )

    # 每个进程负责的帧
    frame_render_process_work_list = []
    # 渲染进程列表
    frame_render_process_list = []
    for process_index in range(now_record["process_total"]):
        frame_render_process_work_list.append(
            range(process_index, video.frame_total, now_record["process_total"])
        )

    for process_index in range(now_record["process_total"]):
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

    # 记录完成
    record.set_now_record("over", True)

    print(time.time() - start_time)
