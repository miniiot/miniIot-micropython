# -*- coding: utf-8 -*-

import sys
import os

import machine
import ubinascii

from .config import Config
from .core.gpio_helper import GPIOHelper
from .core.miniIot_wifi import MiniIotWifi
from .MiniIotMessage import MiniIotMessage


class MiniIot:

    def __init__(self):
        # 主进程工作状态
        self._work_state = 0
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

    def init(self):
        GPIOHelper.init(Config.MiniIot_STATE_LED)
        GPIOHelper.value(Config.MiniIot_STATE_LED, 1)

        MiniIotMessage.setSysCallback(self.sysCallback)

    def init_fs(self):
        try:
            os.umount('/')
            os.VfsLfs2.mkfs(bdev)
            os.mount(bdev, '/')
            print("[SYSTEM] 文件系统格式化成功")
        except:
            print("[SYSTEM] 文件系统格式化失败")

    def init_admin_web_server(self):
        if Config.MiniIot_Admin_Service:
            pass

    def sysCallback(self, dataObj):
        serviceName = dataObj['serviceName']
        if serviceName == "miniiot_wifi_update":
            print("[SYSTEM] 修改wifi")
            if Config.UseWifiClient:
                self.miniIotWifi.update(dataObj["serviceParams"]["ssid"], dataObj["serviceParams"]["passwd"])
                # todo
                machine.reset()

        elif serviceName == "miniiot_ota_update":
            pass

        elif serviceName == "miniiot_admin_update":
            if Config.UseAdminService:
                pass

        elif serviceName == "miniiot_reboot":
            print("[SYSTEM] 重启")
            # todo
            machine.reset()

        else:
            print("[SYSTEM] 未知事件")

    def begin(self, product_id, secret, device_id=None):

        if device_id == None:
            device_id = "A" + ubinascii.hexlify(machine.unique_id()).decode().upper()


        print("[MiniIot] 库版本：" + str(Config.MiniIot_VERSION))
        print("[MiniIot] 程序版本：" + Config.APP_VERSION)
        print("[MiniIot] 产品ID：" + product_id)
        print("[MiniIot] 设备ID：" + device_id)

        self._product_id = product_id
        self._device_id = device_id

        # todo

        self.init()
