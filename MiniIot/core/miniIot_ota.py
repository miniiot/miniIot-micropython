# -*- coding: utf-8 -*-
import os

import ubinascii
import urequests
import ujson
import uhashlib as hashlib


from .miniIot_utils import getDeviceId

class MiniIotOta:

    def __init__(self):
        self._url = ""
        self._file_name = "/"+getDeviceId() + ".mbin"
        self._bin_info = {}

    def begin(self, url: str):
        self._url = url
        if not self._download_bin():
            return
        if not self._read_bin_info():
            return

        if not self._check_bin():
            return




    def _download_bin(self):
        if self._url == "":
            self.on_update_error(-1)
            return False

        try:
            res = urequests.get(self._url)
            if res.status_code != 200:
                self.on_update_error(res.status_code)
                res.close()
                return False
            self.on_update_progress(0, 30)

            with open(self._file_name, "wb") as f:
                f.write(res.content)

            res.close()
            self.on_update_progress(0, 60)
            return True

        except Exception as e:
            self.on_update_error(e)
            return False

    def _check_bin(self):
        h = hashlib.sha256()

        try:
            with open(self._file_name, "rb") as f:
                while True:
                    chunk = f.read(512)  # 分块读取，节省内存
                    if not chunk:
                        break
                    h.update(chunk)

            if ubinascii.hexlify(h.digest()).decode() == self._bin_info["md5"]:
                return True

            return False

        except Exception as e:
            return False




    def _read_bin_info(self):

        try:
            f = open(self._file_name, 'rb')
            info = {"head": 18,
                    "sign": 5,
                    "version": 4,
                    "size": 4,
                    "dateTime": 4,
                    "info_len": 4,
                    "md5":64}
            if f.read(info.get("head")) != b'MiniIotMicroPython':
                return False
            f.read(1)
            self._bin_info['sign'] = f.read(info.get("sign")).decode()
            f.read(1)
            self._bin_info["version"] = int.from_bytes(f.read(info.get("version")), byteorder='big') / 100
            f.read(1)
            self._bin_info["size"] = int.from_bytes(f.read(info.get("size")), byteorder='big')
            f.read(1)
            self._bin_info["dateTime"] = int.from_bytes(f.read(info.get("dateTime")), byteorder='big')
            f.read(1)
            self._bin_info["info_len"] = int.from_bytes(f.read(info.get("info_len")), byteorder='big')
            f.read(1)
            self._bin_info["mpy_info"] = ujson.loads(f.read(self._bin_info["info_len"]).decode())

            # 获取校验值
            file_size = f.seek(0,2)
            f.seek(0, file_size - info['md5'])
            self._bin_info['md5'] = f.read(info["md5"]).decode()
            f.close()
            return True
        except Exception as e:
            self.on_update_error(e)
            return False





    def on_update_started(self):
        pass

    def on_update_finished(self):
        pass

    def on_update_progress(self, state,val):
        pass

    def on_update_error(self, code:int):
        pass