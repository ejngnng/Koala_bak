#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################################
#
# Description: asr parser and mqtt clinet
#
# Author:      ninja
#
# Date:        created by 2017-08-14
#
###################################################

import socket
import jieba
import paho.mqtt.client as mqtt
import json
import sys

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
        "action" : "off",
        "value" : "0"
    }
    if(tokenlist[0] == "打开" or tokenlist[0] == "开" or tokenlist[0] == "开一下"):
        data['action'] = "on"
        data['value'] = "1"

    if(tokenlist[0] == "关闭" or tokenlist[0] == "关一下"):
        data['action'] = "off"
        data['value'] = "0"

    if (tokenlist[1] == "客厅"):
        data["target_id"] = "switch1"


    if(tokenlist[1] == "卧室"):
        data["target_id"] = "switch2"

    if (tokenlist[1] == "厨房"):
        data["target_id"] = "switch3"

    return json.dumps(data)

def main():
	print ("get msg: %s" % (sys.argv[1]))
	getToken(sys.argv[1])

if __name__ == '__main__':
	main()	
