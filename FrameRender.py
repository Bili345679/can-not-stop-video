import cv2
import os
from Video import Video
from BitImg import BitImg
from common import *


class FrameRender(Video):
    def __init__(
        self,
        video_path,
        up_down_val,
        up_bit_list_str,
        down_bit_list_str,
        up_img_move_x,
        up_img_move_y,
        down_img_move_x,
        down_img_move_y,
        start_frame=False,
        end_frame=False,
    ):
        super().__init__(video_path)

        self.video_path = video_path
        self.up_down_val = up_down_val
        self.up_bit_list_str = up_bit_list_str
        self.down_bit_list_str = down_bit_list_str
        self.up_img_move_x = up_img_move_x
        self.up_img_move_y = up_img_move_y
        self.down_img_move_x = down_img_move_x
        self.down_img_move_y = down_img_move_y
        self.start_frame = 0 if start_frame is False else start_frame
        self.end_frame = self.frame_total if end_frame is False else end_frame

        # 临时帧
        self.render_frame_temp_path_list = [
            "./rendered_frame/%s/%s_temp.png"
            % (
                self.video_name,
                str(frame_no).rjust(self.frame_no_len, "0"),
            )
            for frame_no in range(self.frame_total)
        ]

    def render_frame(self, render_range, process_index):
        org_cap = cv2.VideoCapture(self.video_path)

        if process_index == 0:
            start_index = render_range[0]
            start_time = time.time()
            last_time = time.time()

        for frame_index in range(self.frame_total):
            video_read_result, org_frame = org_cap.read()

            # 渲染范围
            # 开始
            if frame_index < self.start_frame:
                continue
            # 结束
            if frame_index > self.end_frame:
                break

            if not video_read_result:
                break

            # 跳过不归自己管的帧
            if not frame_index in render_range:
                continue

            frame_path = self.render_frame_path_list[frame_index]
            frame_temp_path = self.render_frame_temp_path_list[frame_index]

            # 跳过已渲染完成的帧
            if os.path.exists(frame_path):
                if process_index == 0:
                    start_index = frame_index
                    start_time = time.time()
                    last_time = time.time()
                continue

            # 转灰度
            org_frame = cv2.cvtColor(org_frame, cv2.COLOR_BGR2GRAY)

            # 新帧
            rendered_frame_bit_list_list = org_frame.tolist()
            rendered_frame_bit_list = []
            # 移动雪花图
            row_index = 0
            for each_row in rendered_frame_bit_list_list:
                col_index = 0
                for each_bit in each_row:
                    if each_bit < self.up_down_val:
                        x = (
                            frame_index * self.up_img_move_x + col_index
                        ) % self.frame_width
                        y = (
                            frame_index * self.up_img_move_y + row_index
                        ) % self.frame_height
                        bit = self.up_bit_list_str[y * self.frame_width + x]
                    else:
                        x = (
                            frame_index * self.down_img_move_x + col_index
                        ) % self.frame_width
                        y = (
                            frame_index * self.down_img_move_y + row_index
                        ) % self.frame_height
                        bit = self.down_bit_list_str[y * self.frame_width + x]
                    rendered_frame_bit_list.append(bit)

                    col_index += 1
                row_index += 1

            rendered_frame_bit_str = "".join(rendered_frame_bit_list)

            # 新帧图片
            rendered_frame = BitImg(
                self.frame_height, self.frame_width, bit_list_str=rendered_frame_bit_str
            )
            # 保存新帧
            rendered_frame.bit_img_path = frame_temp_path
            rendered_frame.save_bit_img()
            # 重命名
            os.rename(frame_temp_path, frame_path)

            # 进度
            if (
                process_index == 0
                and frame_index != 0
                and (time.time() - last_time) > 1
            ):
                render_frame_count = frame_index - start_index
                spend_time = time.time() - start_time
                frame_avg_spend_time = spend_time / render_frame_count
                remain_frame_count = self.frame_total - render_frame_count
                remain_time = remain_frame_count * frame_avg_spend_time
                end_time = get_data_time(start_time + remain_time)
                ezprint("---------------------------")
                print("帧渲染\t" + str(frame_avg_spend_time) + " 秒/帧")
                print("帧渲染\t" + "剩余帧 " + str(remain_frame_count))
                print("帧渲染\t" + "预计剩余时间 " + str(remain_time))
                print("帧渲染\t" + "预计结束时间 " + str(end_time))
                last_time = time.time()
