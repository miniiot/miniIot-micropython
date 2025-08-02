# -*- coding: utf-8 -*-
import ujson
from umqtt.simple import MQTTClient
import urequests
import uhashlib

from MiniIot.MiniIotMessage import MiniIotMessage
from MiniIot.config import Config
from MiniIot.core.gpio_helper import GPIOHelper


class MiniIotMQTT:

    def __init__(self):
        self._version = ""
        self._bin_info = {}
        self._product_id = ""
        self._device_id = ""
        self._secret = ""
        self._secret_type = ""
        self._mqtt_user = ""
        self._mqtt_passwd = ""
        self._state = False

        self._mqtt_client: MQTTClient = None

    def getNowDateTime(self):
        if Config.UseWifiClient:
            try:
                res = urequests.get("http://" + Config.MiniIot_HTTP_HOST + ":8880/miniiot/device/common/date_time")
            except Exception as e:
                print("[MQTT] 时间获取失败，HTTP连接失败,异常: ",e)
                return "2022-07-07 00:00:00;9527"

            if res.status_code != 200:
                res.close()
                print("[MQTT] 时间获取失败，HTTP代码: " + str(res.status_code))
                return "2022-07-07 00:00:00;9527"

            time_data = res.json()
            res.close()


        if "date_time" not in time_data.keys() or "rand" not in time_data.keys():
            print("[MQTT] 时间解析错误，JSON缺少必要字段")
            return "2022-07-07 00:00:00;9527"

        return time_data['date_time'] + ";" + str(time_data['rand'])


    def getMqttErrorCodeMSg(self,state:int):
        if state == -4:
            return "服务器在保持活动时间内没有响应"
        elif state == -3:
            return "网络连接中断"
        elif state == -2:
            return "网络连接失败"
        elif state == -1:
            return "客户端干净地断开连接"
        elif state == 0:
            return "客户端已连接"
        elif state == 1:
            return "服务器不支持请求的MQTT版本"
        elif state == 2:
            return "服务器拒绝了客户端标识符"
        elif state == 3:
            return "服务器无法接受连接"
        elif state == 4:
            return "用户名/密码被拒绝"
        elif state == 5:
            return "客户端无权连接"
        else:
            return "未知错误[" + str(state) + "]"

    def begin(self, product_id, device_id, secret, secret_type):
        self._product_id = product_id
        self._device_id = device_id
        self._secret = secret
        self._secret_type = secret_type


    def mqttSubscribe(self):
        topic = "sys/" + self._product_id + "/" + self._device_id + "/service"
        try:
            self._mqtt_client.subscribe(topic)
            # self._mqtt_client.subscribe("/ks/")
            print("[MQTT] 主题订阅成功【" + topic + "】")
        except:
            print("[MQTT] 主题订阅失败【" + topic + "】")


    def mqttConnect(self,mac):
        if Config.MiniIot_MQTT_HOST_IS_IP:
            mqtt_host = Config.MiniIot_MQTT_HOST
            print("[MQTT] HOST:",mqtt_host)
        else:
            mqtt_host = self._product_id + "." + Config.MiniIot_MQTT_HOST
        mqtt_client_id = self._product_id + "_" + self._device_id

        GPIOHelper.value(Config.MiniIot_STATE_LED,1)
        self._mqtt_user = self._product_id + ";" + self._device_id + ";" + mac + ";" + self._secret_type + ";1;" + self.getNowDateTime() + ";" + ujson.dumps(self._bin_info)
        self._mqtt_passwd = uhashlib.sha1(self._mqtt_user + ";天才小坑Bi-<admin@dgwht.com>;" + self._secret).digest()
        self._mqtt_passwd = ''.join('{:02x}'.format(b) for b in self._mqtt_passwd)
        print("mqtt_host:",mqtt_host)
        print("mqtt_id:",mqtt_client_id)
        print("matt_uset:",self._mqtt_user)
        print("mqtt_pwd:",self._mqtt_passwd)
        print("[MQTT] MQTT连接中...")
        try:
            self._mqtt_client = MQTTClient(mqtt_client_id, mqtt_host, Config.MiniIot_MQTT_PORT, self._mqtt_user, self._mqtt_passwd)
            self._mqtt_client.set_callback(MiniIotMessage.handleMessage)
            # self._mqtt_client.set_callback(print)
            self._mqtt_client.connect(timeout=30)
            self.mqttSubscribe()
            print("[MQTT] MQTT连接成功")
            self._state = True
            return True
        except Exception as e:
            self._state = False
            print("[MQTT] MQTT连接失败,异常: ",e)
            GPIOHelper.value(Config.MiniIot_STATE_LED, 0)
            return False

    def disconnect(self):
        self._mqtt_client.disconnect()
        self._state = False

    def propertyPost(self, data):
        topic = "sys/" + self._product_id + "/" + self._device_id + "/property"
        try:
            self._mqtt_client.publish(topic, ujson.dumps(data))
            print("[MQTT] 属性上报成功")
        except Exception as e:
            print("[MQTT] 属性上报失败, Error:",e)

    def eventPost(self, data):
        topic = "sys/" + self._product_id + "/" + self._device_id + "/event"
        try:
            self._mqtt_client.publish(topic,data)
            print("[MQTT] 事件上报成功")
        except:
            print("[MQTT] 事件上报失败")

    def loop(self):
        try:
            self._mqtt_client.check_msg()
        except Exception as e:
            self._state = False

    def is_connect(self):
        return self._state