#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import define,options
import logging
import sys
import os
import jieba
import paho.mqtt.client as mqtt
import json
import signal
import threading

settings={
    "debug": True
}

global mqttc
global music_parent_pid
global music_child_pid

def getToken(msg):
    seg_list = jieba.cut(msg, cut_all=False)
    count = 0
    token = []
    for n in seg_list:
        print("token ", count, ": ", n)
        count += 1
        token.append(n)
    return token

def jsonGen(tokenlist):
    data = {
        "name" : "switch",
        "target_id": "switch1",
        "action": "off",
        "value" : "0"
    }
    if(tokenlist[0] == "打开" or tokenlist[0] == "开" or tokenlist[0] == "开一下"):
        data['action'] = "on"
        data['value'] = "1"
    elif(tokenlist[0] == "关闭" or tokenlist[0] == "关一下"):
        data['action'] = "off"
        data['value'] = "0"
    elif(tokenlist[0] == "music"):
        play_music()
        return
    else:
        pass

    if(tokenlist[0] == "关闭" and tokenlist[1] == "音乐"):
        stop_music()
        return

    if(tokenlist[0] == "打开" and tokenlist[1] == "音乐"):
        play_music()
        return

    if(tokenlist[1] == "客厅"):
        data["target_id"] = "switch1"
    elif(tokenlist[1] == "卧室"):
        data["target_id"] = "switch2"
    elif(tokenlist[1] == "厨房"):
        data["target_id"] = "switch3"
    else:
        print("can not understand...")
        return
    return json.dumps(data)

def play_music():
    global music_parent_pid
    global music_child_pid
    print("start music...")
    pid = os.fork()
    if pid:
        music_parent_pid = os.getpid()
        print("parent...", music_parent_pid)
        #os.system("play ~/Music/*.mp3")
    else:
        music_child_pid = os.getpid()
        print("child...", music_child_pid)
        os.system("play ~/Music/*.mp3")
        sys.exit(0)

def kill_process(name):
    res = os.popen("ps -ef | grep %s" % (name))
    for i in res:
        str = i.split()
        if(str[7] == name):
            os.kill(int(str[1]), signal.SIGKILL)
        
def stop_music():
    print("stop music...")
    kill_process('play')


def mqtt_init():
    global mqttc
    mqttc = mqtt.Client("python3_pub")
    mqttc.connect("192.168.1.66", 1883)
    mqttc.loop_start()

def pub_msg(msg):
    global mqttc
    tokenlist = getToken(msg)
    jsonStr = jsonGen(tokenlist)
    mqttc.reconnect()
    mqttc.publish("inTopic", jsonStr)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_argument('asr')
        print(data)
        pub_msg(data)

    def post(self):
        data = self.get_argument('asr')
        print(data)
        pub_msg(data)

def make_app():
    return tornado.web.Application([(r"/", MainHandler)], **settings)


def main():
    args = sys.argv
    args.append("-log_file_prefix=./access.log")
    options.parse_command_line(args)
   # options.parse_config_file("./access.log",'rb')
    mqtt_init()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
