# -*- coding: utf-8 -*-
import network
import os

import time
import ujson
from machine import Pin

from ..config import Config
from .miniIot_utils import exists_file
from .gpio_helper import GPIOHelper

class MiniIotWifi:

    def __init__(self):
        self._connect_time = 0
        self._connect_led_time = 0
        self._config_name = "/wifiConfig.json"

        if Config.DEFAULT_WIFI_SSID != "":
            if Config.DEFAULT_WIFI_PASSWORD != "":
                self._json_data:dict = {"ssid":Config.DEFAULT_WIFI_SSID,
                                   "passwd":Config.DEFAULT_WIFI_PASSWORD}

            else:
                self._json_data = {"ssid": "miniiot.top",
                                   "passwd": "88888888"}
        else:
            self._json_data = {"ssid": "miniiot.top",
                               "passwd": "88888888"}
        self._wlan = network.WLAN(network.STA_IF)

        # self._led_pin = Pin(Config.MiniIot_STATE_LED,Pin.OUT)


    def loadConfig(self):
        if not exists_file(self._config_name):
            print("[WIFI] 无法打开配置文件：")
            print(self._config_name)
            print("[WIFI] 使用默认配置：")
            print(str(self._json_data))
            return False

        try:
            with open(self._config_name,"r") as f:
                self._json_data = ujson.loads(f.read())
            print("[WIFI] 成功读取配置：")
            print(str(self._json_data))
            return True
        except:
            return False


    def write(self):

        try:
            data = ujson.dumps(self._json_data)
            with open(self._config_name, "w") as f:
                f.write(data)
            print("[WIFI] 配置写入成功：")
            print(data)
            return True
        except:
            print("[WIFI] 配置写入失败：")
            print(self._config_name)
            return False

    def wifiConnect(self):
        if self._connect_time == 0:
            self._connect_time = time.ticks_ms()
            self.loadConfig()
            self._wlan.active(True)
            self._wlan.connect(self._json_data['ssid'], self._json_data['passwd'])
            print("[WIFI] WIFI连接中")

        if self._connect_led_time == 0:
            self._connect_led_time = time.ticks_ms()
            print(".")
            # self._led_pin.value(0 if self._led_pin.value() == 1 else 1)
            GPIOHelper.toggle(Config.MiniIot_STATE_LED)

        if self._wlan.status() != network.STAT_CONNECTING:
            if time.ticks_ms() - self._connect_led_time >= 1000:
                self._connect_led_time = 0
            if time.ticks_ms() - self._connect_time >= 10*1000:
                print("")
                print("[WIFI] WIFI连接超时")
                self._connect_time = 0

            return False

        print("")
        print("[WIFI] WIFI连接成功,IP: ")
        print(self._wlan.ifconfig()[0])
        # print("[WIFI] WIFI连接成功,MAC: ")
        # print(self._wlan.ifconfig())
        self._connect_time = 0
        return True

    def getWifiMac(self):
        return self._wlan.config("mac")

    def getStatus(self):
        return self._wlan.status()

    def clear(self):
        if not exists_file(self._config_name):
            print("[WIFI] 配置不存在")
            return
        os.remove(self._config_name)
        print("[WIFI] 配置清除成功：")
        print(self._config_name)


    def update(self,ssid, passwd):
        self._json_data['ssid'] = ssid
        self._json_data['passwd'] = passwd
        self.write()

