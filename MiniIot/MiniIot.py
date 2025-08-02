# -*- coding: utf-8 -*-

import sys
import os
import gc
import machine
import time
import ubinascii
import network
import utime

from .config import Config, WorkState
from .core.gpio_helper import GPIOHelper
from .core.miniIot_wifi import MiniIotWifi
from .MiniIotMessage import MiniIotMessage
from .MiniIotMQTT import MiniIotMQTT


class MiniIot:

    def __init__(self):
        # 主进程工作状态
        self._work_state = WorkState.INIT
        # 服务器重连次数
        self._server_err_num = 0
        # mqtt重连间隔
        self._server_reconnect_time = 2000
        # mqtt重连时间
        self._server_connect_time = 0
        # 产品ID
        self._product_id = ""
        # 设备ID
        self._device_id = ""

        self.miniIotWifi = MiniIotWifi()
        self.miniIotClient = MiniIotMQTT()

    def init(self):
        GPIOHelper.init(Config.MiniIot_STATE_LED)
        GPIOHelper.value(Config.MiniIot_STATE_LED, 1)

        MiniIotMessage.setSysCallback(self.sysCallback)

    def init_fs(self):
        '''不可用'''
        return
        try:
            os.umount('/')
            os.VfsLfs2.mkfs(bdev)
            os.mount(bdev, '/')
            print("[SYSTEM] 文件系统格式化成功")
        except Exception as e:
            print("[SYSTEM] 文件系统格式化失败, error:", e)

    def init_admin_web_server(self):
        if Config.MiniIot_Admin_Service:
            pass

    def sysCallback(self, dataObj):
        serviceName = dataObj['serviceName']
        if serviceName == "miniiot_wifi_update":
            print("[SYSTEM] 修改wifi")
            if Config.UseWifiClient:
                self.miniIotWifi.update(dataObj["serviceParams"]["ssid"], dataObj["serviceParams"]["password"])
                self.miniIotClient.disconnect()
                self.miniIotWifi.disconnect()
                machine.reset()


        elif serviceName == "miniiot_ota_update":
            pass

        elif serviceName == "miniiot_admin_update":
            if Config.UseAdminService:
                pass

        elif serviceName == "miniiot_reboot":
            print("[SYSTEM] 重启")
            self.miniIotClient.disconnect()
            machine.reset()

        else:
            print("[SYSTEM] 未知事件")

    def begin(self, product_id, secret, device_id=None):
        secret_type = "2"
        if device_id == None:
            device_id = "P" + str(ubinascii.hexlify(machine.unique_id()).decode().upper())[0:8] + "Z"
            secret_type = "1"

        print("[MiniIot] 库版本:" + str(Config.MiniIot_VERSION))
        print("[MiniIot] 程序版本:" + Config.APP_VERSION)
        print("[MiniIot] 产品ID:" + product_id)
        print("[MiniIot] 设备ID:" + device_id)

        self._product_id = product_id
        self._device_id = device_id

        self.miniIotClient.begin(product_id, device_id, secret, secret_type)

        self.init()

    def attach(self, func):
        MiniIotMessage.setAppCallback(func)

    def loop(self):
        if Config.UseAdminService:
            pass

        if self._work_state == WorkState.INIT:
            self._work_state = WorkState.NETWORK_CONNECTING

        elif self._work_state == WorkState.NETWORK_CONNECTING:
            if Config.UseWifiClient:
                if self.miniIotWifi.wifiConnect() == True:
                    self._server_reconnect_time = 1000 * 2
                    self._server_err_num = 0
                    self._work_state = WorkState.SERVER_CONNECTING
                else:
                    self._work_state = WorkState.NETWORK_ERROR
            else:
                pass

        elif self._work_state == WorkState.SERVER_CONNECTING:
            if Config.UseWifiClient:
                if self.miniIotClient.mqttConnect(self.miniIotWifi.getWifiMac()):
                    self._server_err_num = 0
                    self._work_state = WorkState.WORKING
                else:
                    self._server_err_num += 1
                    self._work_state = WorkState.SERVER_ERROR
            else:
                pass

        elif self._work_state == WorkState.WORKING:
            self.miniIotClient.loop()
            if not self.miniIotClient.is_connect():
                if Config.UseWifiClient:
                    if self.miniIotWifi.getStatus() != network.STAT_GOT_IP:
                        self._work_state = WorkState.NETWORK_ERROR
                    else:
                        self._work_state = WorkState.SERVER_ERROR
                else:
                    pass

        elif self._work_state == WorkState.SERVER_ERROR:
            if self._server_err_num > 5:
                self._server_reconnect_time = 1000 * 30
            if time.ticks_ms() - self._server_connect_time > self._server_reconnect_time:
                self._work_state = WorkState.SERVER_CONNECTING
                self._server_connect_time = time.ticks_ms()
            if Config.UseWifiClient:
                if self.miniIotWifi.getStatus() != network.STAT_GOT_IP:
                    self._work_state = WorkState.NETWORK_ERROR
            else:
                pass

        elif self._work_state == WorkState.NETWORK_ERROR:
            self._work_state = WorkState.NETWORK_CONNECTING

    def running(self):
        return self._work_state == WorkState.WORKING

    def delay(self, ms: int):
        start = time.ticks_ms()
        while time.ticks_ms() - start < ms:
            if self._work_state == WorkState.WORKING:
                self.loop()
            utime.sleep(0)

    def propertyPost(self, property_name: str, property_value):

        data = {"id": 0, "version": "1.0",
                "method": "property.post",
                "sys": {"ack": 0, "product": self._product_id,
                        "device": self._device_id
                        },
                "params": {
                    property_name: {"value": property_value}
                }
                }

        self.miniIotClient.propertyPost(data)
