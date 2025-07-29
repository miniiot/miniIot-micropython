# -*- coding: utf-8 -*-
from machine import Pin


class GPIOHelper:
    _pins = {}

    @staticmethod
    def init(pin_num, mode=Pin.OUT):
        if pin_num not in GPIOHelper._pins:
            GPIOHelper._pins[pin_num] = Pin(pin_num, mode)

    @staticmethod
    def on(pin_num):
        pin = GPIOHelper._pins.get(pin_num)
        if pin:
            pin.on()
        else:
            raise RuntimeError(f"Pin {pin_num} not initialized")

    @staticmethod
    def off(pin_num):
        pin = GPIOHelper._pins.get(pin_num)
        if pin:
            pin.off()
        else:
            raise RuntimeError(f"Pin {pin_num} not initialized")

    @staticmethod
    def toggle(pin_num):
        pin = GPIOHelper._pins.get(pin_num)
        if pin:
            pin.value(1 - pin.value())
        else:
            raise RuntimeError(f"Pin {pin_num} not initialized")

    @staticmethod
    def value(pin_num, val=None):
        pin = GPIOHelper._pins.get(pin_num)
        if not pin:
            raise RuntimeError(f"Pin {pin_num} not initialized")
        if val is None:
            return pin.value()
        pin.value(val)
