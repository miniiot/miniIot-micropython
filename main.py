from MiniIot import MiniIot,GPIOHelper


def serviceCallbackFunction(data):
    print(data)




if __name__ == '__main__':
    print("----------")
    miniIot = MiniIot()
    miniIot.begin("ZnnQmFTH","h5Tmn1l3m2S9DY2I")
    miniIot.attach(serviceCallbackFunction)

    while True:
        miniIot.loop()

        if miniIot.running():
            miniIot.delay(3000)
