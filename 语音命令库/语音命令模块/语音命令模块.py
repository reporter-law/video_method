"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import glob
import sys
import wave,os,shutil
import pyaudio
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from aip import AipSpeech
import re
import numpy as np
from jieba import posseg as psg
from fuzzywuzzy import process



r = sr.Recognizer()

class Sound_from_text():
    def __init__(self):
        self.output_sound_file = sys.argv[0].split(".")[0] + "\语音输出文件"

    def TTS(self,text, speed, lan, per):
        """文本转语音输出"""
        convertTable = {'中文': ('ZH', {'标准女音': 0, '标准男音': 1, '斯文男音': 3,
                                      '小萌萌': 4, '知性女音': 5, '老教授': 6, '葛平音': 8, '播音员': 9, '京腔': 10,
                                      '温柔大叔': 11}),
                        '英式英语': ('UK', {'标准音': 0}), '美式英语': ('EN', {'标准音': 0}),
                        '粤语': ('CTE', {'标准音': 0})}
        data = {'tex': text, 'spd': speed, 'lan': convertTable[lan][0],
                'per': convertTable[lan][1][per], 'ctp': 1, 'cuid': 'baike', 'ie': 'UTF-8',
                'pdt': 301, 'vol': 9, 'rate': 40}
        result = requests.get('https://tts.baidu.com/text2audio', params=data)
        try:
            result.json()
        except:
            return result.content
        else:
            raise ValueError

    def sound(self,text):
        try:
            bindata = self.TTS(text, 6, '中文', '知性女音')
            with open(self.output_sound_file  + 'result.wav', 'wb+') as f:
                f.write(bindata)
            song = AudioSegment.from_mp3(self.output_sound_file + 'result.wav')
            play(song)
        except:
            print('\r出现不明错误！！！！！')


class Sound_recognition():
    def __init__(self):
        self.r =sr.Recognizer()
        self.s = Sound_from_text().sound
        self.sound_file = sys.argv[0].split(".")[0] + "\命令文件"

    def baidu_sound(self,file):
        """百度语音识别"""
        APP_ID = '19236313'
        API_KEY = 'gZ4E58quu5HgFalbda9ktNl7'
        SECRET_KEY = 'QzGPaVmFUQoSZGO1zbr18MAzldmKY01K'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        if file.split(".")[1] == "wav":
            # 识别本地文件
            with open(file, 'rb') as fp:
                audio = fp.read()
            result = client.asr(audio, 'wav', 16000, {'dev_pid': 1537, })  # 关键为1537而非1536
            text = "音频文件格式正确，可以直接进行语音识别"
            #self.s(text)
            return result['result'][0]
        else:
            """格式转换"""
            text = "音频文件转换中，请继续等待,音频文件格式为：{type}".format(type=file.split(".")[1])
            self.s(text)
            audio_file = AudioSegment.from_file(file, format=file.split(".")[1])
            path = self.sound_file+"\record_1.wav"
            audio_file.export(path, format="wav")
            with open(path, 'rb') as fp:
                audio = fp.read()
            result = client.asr(audio, 'wav', 16000, {'dev_pid': 1537, })  # 关键为1537而非1536
            text = "音频文件格式转换后再次进行语音识别中，请等待"
            self.s(text)
            return result['result'][0]




    """谷歌语音识别，speech版本"""
    def speech_google(self,file):
        """语音识别"""
        if file.split(".")[1] == "flac" or file.split(".")[1] == "wav":
            command= file.split(".")[0].split("\\")[-1]
            #text = "{}进行语音识别中".format(command)
            #s(text)
            #os.startfile(r"F:\迅雷下载\ant_1.3.4\ant.exe")
            """文件读取"""
            audio_file = file.strip('\u202a')
            with sr.AudioFile(audio_file) as source:
                audio = self.r.record(source)
            try:
                return self.r.recognize_google(audio, language='zh_CN')
            except:
                res = self.r.recognize_google(audio, language='zh_CN',show_all=True)  # 汉语
                return res["alternative"][0]["transcript"]

            # print('文本内容: ', r.recognize_sphinx(audio))  # 英语
        else:
            """格式转换"""
            text = "音频文件错误，转换中，请等待,音频文件格式为：{type}".format(type=file.split(".")[1])
            self.s(text)
            try:
                audio_file = AudioSegment.from_file(file, format=file.split(".")[1])
                path = self.sound_file+"\record_1.flac"
                audio_file.export(path, format="flac")
            except:
                text = "请注意，pydub模块不能对pcm格式进行转换"
                self.s(text)
            else:
                self.speech_google(path)



class Text_from_recoding():
    def __init__(self):
        self.s = Sound_from_text().sound
        self.sg = Sound_recognition().speech_google
        self.sound_file = sys.argv[0].split(".")[0] + "\语音文件"

    def recording(self,filename, i):
        """官方录音教程,,增加了音量以及时间计算的录音退出功能
        """
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100  # 读取速度
        RECORD_SECONDS = 5  # 记录秒数
        second = 10
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        # 语音说明

        if i%2==0:#除法都是浮点数

            text = "\r是否退出程序？"
        else:
            text = "\r开始聆听命令：............................"
        self.s(text)
        print(text, end="\t")

        frames = []  # 录音列表

        """计时计算"""
        volume_start = time.time()
        timeout_start = time.time()
        global across
        while True:
            """实际运行时间"""

            timer = time.perf_counter()  # 程序运行计时器
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.short)

            temp = np.max(audio_data)
            """如果音量小于1000的时间持续10秒就会结束"""
            if temp < 1000:
                volume_end = time.time()
                volume_time = volume_end - volume_start
                if volume_time > 5:
                    text = "\r经命令读取程序判断，退出.......音量{}.........".format(temp)
                    #self.s(text)
                    print(text,end="")
                    break
            else:
                volume_start = time.time()
                """程序总历时10秒也结束"""
            timeout_end = time.time()
            timeout = timeout_end - timeout_start
            if timeout > 10:
                text = "\r命令读取程序超时退出.......音量数字为{}.........".format(temp)
                #self.s(text)
                print(text,end="")
                break
        print("\r程序已经运行了{}".format(timer), end="")

        # 计算实际程序耗时，包括音量小退出
        actual_timeend = time.time()
        actual_time = actual_timeend - timeout_start
        text = "\r命令读取结束...........命令时长：{across}秒.......".format(across=int(actual_time))
        #self.s(text)
        print(text,end="")

        """存储写入"""
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def thread_record(self):
        """implement 多次录音"""
        i = 1
        """文件清理"""
        path = self.sound_file+"\命令文件"
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)
        while True:
            text = "\r第%d个命令听取准备中..................." % i
            #s(text)
            print(text,end="")
            filename = path + r'\第%d个命令.wav' % i
            self.recording(filename, i)
            """对录音是否继续继续确认"""

            file_confire = self.sound_file+"\确认语音.wav"

            i += 1#保障语音输出

            self.recording(file_confire,i)

            """继续语音识别"""
            condition = self.sg(file_confire)
            print("\r语音命令为："+condition,end="\n")
            exit_ = ["不继续", "结束", "不进行", "不", "退出", "滚"]
            for i_ in exit_:
                if i_ in condition:
                    text = "命令读取程序自此退出，将进入命令执行程序"
                    self.s(text)
                    return path
            else:
                i += 1#保障语音输出


class Command_manager():
    def __init__(self):
        pass

        self.word = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                                '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}

    def chinese2digits(self,uchars_chinese):
        """纯粹中文数字转阿拉伯"""
        total = 0
        r = 1  # 表示单位：个十百千...
        """倒着遍历"""
        for i in range(len(uchars_chinese) - 1, -1, -1):
            val = self.word.get(uchars_chinese[i])
            if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
                    # total =total + r * x
            elif val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            else:
                total = total + r * val
        return total

    def chinese_math(self,need_change):
        """注意单位：此时是月"""
        # word将中文数字转拉伯数字
        # print(type(need_change))存在空值的need_change
        global china_math
        china_math = []
        if type(need_change).__name__ == "str":
            pass
        else:
            need_change = str(need_change)
        try:
            math = re.findall("\d+", need_change)[0]
            china_math.append(int(math))
        except:
            pass
        for i, key in enumerate(list(need_change)):
            # 切割字符串，将key作为判断,判断传入转换的数字
            if key in self.word.keys():
                math = self.chinese2digits(key)
                china_math.append(math)
        if len(china_math) <= 1:
            if type(china_math[0]).__name__ == "int":
                china_math = list(str(china_math[0]))
            else:
                china_math = list(china_math[0])
        math = np.bincount(china_math)
        math = np.argmax(math)
        return int(math)
    def chinese_simple_command(self,command):
        """对简单中文命令进行处理"""
        """
        fre = {}
        command = []
        for i in list(command):
            if i in fre:
                fre[i] += 1
            else:
                fre[i] = 1
        for number, i in enumerate(fre.values()):
            if i > 1:
                pass
            else:
                command.append(list(fre.keys())[number])
        return ''.join(command)
        """
        return command
    def chinese_complex_command(self,command,file_path):
        """中文复杂命令，切词以及模糊匹配,file_path为语料库"""

        city = []
        commands = []
        for x in psg.lcut(command.strip()):
            if x.flag in ['n', 'nr', 'ns'] and len(x.word) > 1:
                city.append(x.word)

        for city in city:
            with open(file_path, "r",encoding="utf-8")as f:
                a = f.read()
                content = re.findall(r'[\u4e00-\u9fa5]+', a)
                content = process.extract(city, content)
                for i in content:
                    if i[1] >= 90:
                        commands.append(city)
        if len(commands) <=1:
            return commands
        else:
            print("提示：可能存在多个有意义的命令")
            return commands




def command_speak():
    global commands
    tr = Text_from_recoding().thread_record
    Sr = Sound_recognition
    s = Sound_from_text().sound
    path = tr()
    path_list = glob.glob(os.path.join(path,"*"))
    #print("当前命令录音所在地址为： ",path_list)
    if len(path_list) == 1:
        try:
            command= [Sr().speech_google(path_list[0])]

            commands = Command_manager().chinese_simple_command(command)#命令处理程序
        except:
            print("\r识别出错",end="")
    else:
        text="语音命令有多条，将逐一执行，注意返回命令为列表"
        s(text)
        commands = []
        for path in path_list:
            command =Sr().speech_google(path)
            command = Command_manager().chinese_simple_command(command)
            commands.append(command)


    return commands


