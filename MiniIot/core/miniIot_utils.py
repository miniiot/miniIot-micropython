# -*- coding: utf-8 -*-
import os


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
