"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from pydub import AudioSegment
from ffmpeg import audio


class Pydub_method():
    def __init__(self,path1,path2,path3):
        # 1秒=1000毫秒
        self.SECOND = 1000#单位必须是毫秒
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3



    def get_audio(self,start_time,end_time):
        """音频剪辑"""
        song = AudioSegment.from_file(self.path1, format="mp3")
        # song_ = AudioSegment.from_file(r"J:\\vedio\\manager\\audio\\千秋令和朝代歌\\弥撒与千秋令混合.mp3", format="mp3")-6
        # song_ =song_.fade_in(5000).fade_out(5000)
        # newsong_1 = song[:55*SECOND]
        # newsong = newsong_1+song_+ song[60*SECOND:]
        newsong = song[start_time* self.SECOND:end_time * self.SECOND]
        newsong.export(self.path2)

    def audio_concat(self):
        """音频混合"""
        sound1 = AudioSegment.from_file(self.path1) - 1
        sound2 = AudioSegment.from_file(self.path2) - 6
        sound2.fade_in(5000).fade_out(5000)

        played_togther = sound1.overlay(sound2)
        played_togther.export(self.path3)

    def audio_fade(self,start_time,end_time):
        """音频淡入淡出"""
        song= AudioSegment.from_file(self.path1)
        song_1 = song.fade_in(start_time*self.SECOND).fade_out(end_time*self.SECOND)
        song_1.export(self.path2)


    def audio_fast(self,speed):
        """音频加速，没有找到pydub中的音频加速"""
        audio.a_speed(self.path1, speed, self.path2)







