import utime

from MiniIot import MiniIot,GPIOHelper

ping_count = 0

def serviceCallbackFunction(data:dict):
    global ping_count, miniIot
    serviceName = data["serviceName"]
    if serviceName == "miniiot_ping":
        miniIot.propertyPost("num_1",ping_count)
        ping_count+=1


if __name__ == '__main__':
    miniIot = MiniIot()
    miniIot.begin("MHHAABQc","jNrE1bdPIQk3SeeV")
    miniIot.attach(serviceCallbackFunction)

    while True:
        miniIot.loop()

        if miniIot.running():
            # miniIot.delay(3000)
            utime.sleep_ms(1000)

