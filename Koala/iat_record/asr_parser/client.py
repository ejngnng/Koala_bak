#!/usr/bin/env python3
#-*- coding=utf-8 -*-

import requests
import sys

def main():
    data = {
        'asr': sys.argv[1]
    }
    url = "http://192.168.1.66:8888/"
    print ("send request..")
    requests.get(url, params=data)
    

if __name__=="__main__":
    main()

