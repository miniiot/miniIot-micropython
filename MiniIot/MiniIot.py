# -*- coding: utf-8 -*-

import sys
import os

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

    def init(self):
        pass

    def init_fs(self):
        try:
            os.umount('/')
            os.VfsLfs2.mkfs(bdev)
            os.mount(bdev, '/')
            print("[SYSTEM] 文件系统格式化成功")
        except:
            print("[SYSTEM] 文件系统格式化失败")

    def init_admin_web_server(self):
        pass


