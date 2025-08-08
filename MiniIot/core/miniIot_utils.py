# -*- coding: utf-8 -*-
import os
import machine
import ubinascii

def exists_file(path: str) -> bool:
    """
    Check if the file exists
    :param path:
    :return:
    """
    try:
        mode = os.stat(path)[0]
        if mode & 0x4000:
            return False
        return True
    except OSError as e:
        return False


def getDeviceId():
    return str(ubinascii.hexlify(machine.unique_id()).decode().upper())
