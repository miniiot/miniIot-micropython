# -*- coding: utf-8 -*-
from enum import IntEnum

class Config:
    APP_VERSION: str = "all_2506091055"
    MiniIot_VERSION: str = ""

    DEFAULT_WIFI_SSID: str = ""
    DEFAULT_WIFI_PASSWORD: str = ""

    SYS_RST_IO: int = 0

    MiniIot_STATE_LED: int = 0
    MiniIot_ADMIN_SERVICE_PORT: int = 10101

    MiniIot_HTTP_HOST: str = "service.miniiot.top"
    MiniIot_MQTT_HOST_IS_IP: bool = True
    MiniIot_MQTT_HOST: str = "mqtt.miniiot.top"
    MiniIot_MQTT_PORT: int = 2082

    MiniIot_Admin_Service: bool = True
    UseWifiClient: bool = True
    UseAdminService: bool = True


class WorkState(IntEnum):
    INIT = 100
    NETWORK_CONNECTING = 101
    SERVER_CONNECTING = 102
    WORKING = 103
    SERVER_ERROR = 104
    NETWORK_ERROR = 105


