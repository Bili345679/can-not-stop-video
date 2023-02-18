import cv2
from common import *
import ffmpeg


class Video:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_name = get_file_name(video_path)

        # 读取视频信息
        self.load_org_video()

        # 帧保存地址
        self.render_frame_dir = "./rendered_frame/%s" % (self.video_name)
        mk_dir(self.render_frame_dir)
        # 完成帧
        self.render_frame_path_list = [
            "./rendered_frame/%s/%s.png"
            % (
                self.video_name,
                str(frame_no).rjust(self.frame_no_len, "0"),
            )
            for frame_no in range(self.frame_total)
        ]

    # 加载视频信息
    def load_org_video(self):
        if not os.path.exists(self.video_path):
            raise ("文件不存在")

        # 原视频
        org_cap = cv2.VideoCapture(self.video_path)
        # 总帧数
        self.frame_total = int(org_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # self.frame_total = 500
        # 帧文件数字长度
        self.frame_no_len = len(str(self.frame_total))
        # 帧率
        self.frame_rate = org_cap.get(cv2.CAP_PROP_FPS)
        # 帧高度
        self.frame_height = int(org_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 帧宽度
        self.frame_width = int(org_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ezprint("video_load_over")


    # 合并视频
    def render_video(self):
        # 视频信息
        video_save_path = "./over_video/%s.mp4" % (self.video_name)
        video_without_audio_path = "./over_video/%s_without_audio.mp4" % (
            self.video_name
        )
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        video = cv2.VideoWriter(
            video_without_audio_path,
            fourcc,
            self.frame_rate,
            (self.frame_width, self.frame_height),
        )

        # 合成视频
        for frame_index in range(self.frame_total):
            frame = cv2.imread(self.render_frame_path_list[frame_index])
            video.write(frame)
            if frame_index % 100 == 0:
                ezprint("合成视频\t" + self.render_frame_path_list[frame_index])

        video.release()

        new_video = ffmpeg.input(video_without_audio_path)
        video_track = new_video.video.hflip()
        org_video = ffmpeg.input(self.video_path)
        audio_track = org_video.audio
        video_with_audio = ffmpeg.output(audio_track, video_track, video_save_path)
        ffmpeg.run(video_with_audio)

        os.remove(video_without_audio_path)

    # 删除帧
    def remove_render_frame(self):
        for each_frame_path in self.render_frame_path_list:
            remove_file_folder(each_frame_path)
        # remove_file_folder(self.render_frame_dir)
