# -*- coding: utf-8 -*-

class Config:
    APP_VERSION: str = "all_2506091055"
    MiniIot_VERSION: str = ""

    DEFAULT_WIFI_SSID: str = "Xiaomi_7915"
    DEFAULT_WIFI_PASSWORD: str = "ks123456"

    SYS_RST_IO: int = 0

    MiniIot_STATE_LED: int = 2
    MiniIot_ADMIN_SERVICE_PORT: int = 10101

    MiniIot_HTTP_HOST: str = "service.miniiot.top"
    MiniIot_MQTT_HOST_IS_IP: bool = False
    MiniIot_MQTT_HOST: str = "mqtt.miniiot.top"
    MiniIot_MQTT_PORT: int = 2082

    MiniIot_Admin_Service: bool = True
    UseWifiClient: bool = True
    UseAdminService: bool = True


class WorkState:
    INIT = 100
    NETWORK_CONNECTING = 101
    SERVER_CONNECTING = 102
    WORKING = 103
    SERVER_ERROR = 104
    NETWORK_ERROR = 105


