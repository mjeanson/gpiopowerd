#!/usr/bin/env python
#
# Copyright (C) 2016 - Michael Jeanson <mjeanson@efficios.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

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
    PROMPT = "> "

    @command(['list', 'ls'])
    def command_list(self, params):
        '''
        List the available boards
        '''
        self.writeresponse('''1: lava-armhf-wandboard-01 (7001)
2: lava-armhf-wandboard-02 (7002)
3: ci-node-armhf-01 (7003)
4: ci-node-armhf-02 (7004)
''')

    @command(['on'])
    def command_on(self, params):
        '''<board id>
        Turn on the specified board
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except (ValueError, IndexError):
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
        '''<board id>
        Turn off the specified board
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except (ValueError, IndexError):
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
        '''<board id>
        Reset the specified board
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except (ValueError, IndexError):
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
        '''<board id>
        Get the status of the specified board
        '''
        try:
            device_number = int(params[0])
            gpio = DEVICES[device_number]
            gpio_path = "/sys/class/gpio/%s/value" % gpio
        except (ValueError, IndexError):
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

def run():
    server = TelnetServer((HOST, PORT), MyHandler)
    server.serve_forever()
