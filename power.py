from telnetsrv.threaded import TelnetHandler, command
import SocketServer
import os.path
import time

HOST = ""
PORT = 23

GPIO_ON  = 0
GPIO_OFF = 1

DEVICES = {
    1: "gpio66",
    2: "gpio67",
    3: "gpio69",
    4: "gpio68"
}

PATH = "/sys/class/gpio/%s/value"



class MyHandler(TelnetHandler):
    WELCOME = "carrier-armhf power control"

    @command(['list', 'ls'])
    def command_list(self, params):
        '''
        '''
        self.writeresponse('''1: lava-armhf-wandboard-01 (7001)
2: lava-armhf-wandboard-02 (7002)
3: ci-node-armhf-01 (7003)
4: ci-node-armhf-01 (7004)
''')

    @command(['on'])
    def command_on(self, params):
        '''
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except ValueError:
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+b', 0) as f:
            value = int(f.readline())
            if value == GPIO_ON:
                self.writeresponse("Power is already on")
            else:
                f.write(str(GPIO_ON))
                self.writeresponse("Power set to on")

        return


    @command(['off'])
    def command_off(self, params):
        '''
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except ValueError:
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+b', 0) as f:
            value = int(f.readline())
            if value == GPIO_OFF:
                self.writeresponse("Power is already off")
            else:
                f.write(str(GPIO_OFF))
                self.writeresponse("Power set to off")

        return


    @command(['reset'])
    def command_reset(self, params):
        '''
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except ValueError:
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+b', 0) as f:
            f.write(str(GPIO_OFF))
            time.sleep(0.5)
            f.write(str(GPIO_ON))
            self.writeresponse("Power was reset")
        return

    @command(['status'])
    def command_status(self, params):
        '''
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except ValueError:
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+b', 0) as f:
            value = int(f.readline())
            if value == GPIO_ON:
                self.writeresponse("Power is ON")
            else:
                self.writeresponse("Power is OFF")

        return

class TelnetServer(SocketServer.TCPServer):
    allow_reuse_address = True

server = TelnetServer((HOST, PORT), MyHandler)
server.serve_forever()
