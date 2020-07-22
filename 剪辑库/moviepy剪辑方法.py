"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from moviepy.editor import *

class Moviepy_method():
    def __init__(self,path1,path2,path3="‪J:\vedio",path4 = "‪J:\vedio\original"):
        self.input_path = path1.strip("\u202a")
        self.path2 = path2.strip("\u202a")
        self.path3 = path3.strip("\u202a")
        self.path4 = path4.strip("\u202a")

    def Getaudio(self):
        """音频提取"""
        vedio1 = VideoFileClip(self.input_path.strip("\u202a"))
        audio1 = vedio1.audio
        audio1.write_audiofile(self.path2)


    def getvideo(self,start_time,end_time):
        """视频提取"""
        vedio1 = VideoFileClip(self.input_path)
        # vedio2 = vedio1.without_audio()
        video2 = vedio1.subclip(start_time, end_time)
        # video4 = vedio2.subclip(9,-1)
        video2.write_videofile(self.path2)


    def video_fast(self,number):
        """视频加速"""
        clipVideo = VideoFileClip(self.input_path)
        newclip = clipVideo.fl_time(lambda t: number * t, apply_to=['mask'], keep_duration=True)
        duration = int(clipVideo.duration / 2)
        newclip = newclip.subclip(0,duration)
        newclip.write_videofile(self.path2)

    def video_drop(self):
        """视频无声"""
        video = VideoFileClip(self.input_path)
        video = video.without_audio()
        video.write_videofile(self.path2)

    def video_concat(self):
        """视频合成"""
        video1 = VideoFileClip(self.input_path).fx(vfx.resize, width=848)
        video2 = VideoFileClip(self.path2).fx(vfx.resize, width=848)
        video3 = VideoFileClip(self.path3).fx(vfx.resize, width=848)
        # video4 = VideoFileClip(path4)
        final_clip = concatenate_videoclips([video1, video2, video3], method="compose")
        final_clip.to_videofile(self.path4, fps=24, remove_temp=False)

    def audio_concat_vedio(self,audio_path):
        """音频视频合成"""
        video = VideoFileClip(self.path)
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)  # 不能直接是audio的路径
        video.write_videofile(self.path2)

path =  r"‪‪J:\\vedio\\manager\\past_now_future11.mp4"
output_path = r"J:\vedio\original\diqiu.mp4"
path3 = r"‪J:\\vedio\\manager\\past_now_future22.mp4‪"
path4 = r"‪J:\\vedio\\manager\\past_now_future.mp4"
command = Moviepy_method(path,output_path,path3,path4).video_concat()
