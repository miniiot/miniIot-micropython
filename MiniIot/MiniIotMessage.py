# -*- coding: utf-8 -*-
import ujson


class MiniIotMessage:
    _app_callback = None
    _sys_callback = None

    @classmethod
    def setAppCallback(cls,func):
        cls._app_callback = func

    @classmethod
    def setSysCallback(cls,func):
        cls._sys_callback = func

    @classmethod
    def handleMessage(cls, topic, payload):

        print("[MQTT] 收到消息：\n主题: " + str(topic) + "\n内容:" + str(payload))

        try:
            msg_data = ujson.loads(payload)
        except :
            print("[MQTT] JSON解析错误: " + str(payload))
            return

        for key in msg_data.keys():
            if key not in ["id", "version", "method", "params"]:
                print("[MQTT] JSON缺少必要字段")
                return

        if msg_data['version'] != "1.0":
            print("[MQTT] 协议版本不支持")
            return

        if msg_data['method'] == "service.control.sys":
            if cls._sys_callback is not None:
                cls._sys_callback(msg_data['params'])
        elif msg_data['method'] == "service.control":
            if cls._app_callback is not None:
                cls._app_callback(msg_data['params'])
        else:
            print("[MQTT] 未知method")
