# Copyright (C) 2019 Michael Jeanson <mjeanson@efficios.com>
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

from telnetsrv.threaded import TelnetHandler, command
import os.path
import time

GPIO_PATH = "/sys/class/gpio/gpio%d/value"
GPIO_ON  = 0
GPIO_OFF = 1

class GPIOPowerdHandler(TelnetHandler):
    def __init__(self, request, client_address, server):
        self.WELCOME = server.config.welcome
        self.PROMPT = server.config.prompt
        self.config = server.config

        TelnetHandler.__init__(self, request, client_address, server)

    @command(['list', 'ls'])
    def command_list(self, params):
        '''
        List the available devices
        '''

        for (k, v) in self.config.devices.items():
            self.writeresponse("%d: %s (%s)" % (k, v.name, v.port))

    @command(['on'])
    def command_on(self, params):
        '''<device id>
        Turn on the specified device
        '''
        try:
            device_number = int(params[0])
            gpio = self.config.devices[device_number].gpio
            gpio_path = GPIO_PATH % gpio
        except (ValueError, KeyError):
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+') as f:
            value = int(f.readline())
            if value == GPIO_ON:
                self.writeresponse("Power is already on")
            else:
                f.write(str(GPIO_ON))
                f.flush()
                self.writeresponse("Power set to on")

        return


    @command(['off'])
    def command_off(self, params):
        '''<device id>
        Turn off the specified device
        '''
        try:
            device_number = int(params[0])
            gpio = self.config.devices[device_number].gpio
            gpio_path = GPIO_PATH % gpio
        except (ValueError, KeyError):
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+') as f:
            value = int(f.readline())
            if value == GPIO_OFF:
                self.writeresponse("Power is already off")
            else:
                f.write(str(GPIO_OFF))
                f.flush()
                self.writeresponse("Power set to off")

        return


    @command(['reset'])
    def command_reset(self, params):
        '''<device id>
        Reset the specified device
        '''
        try:
            device_number = int(params[0])
            gpio = self.config.devices[device_number].gpio
            gpio_path = GPIO_PATH % gpio
        except (ValueError, KeyError):
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+') as f:
            f.write(str(GPIO_OFF))
            f.flush()
            time.sleep(0.5)
            f.write(str(GPIO_ON))
            f.flush()
            self.writeresponse("Power was reset")
        return


    @command(['status'])
    def command_status(self, params):
        '''<device id>
        Get the status of the specified device
        '''
        try:
            device_number = int(params[0])
            gpio = self.config.devices[device_number].gpio
            gpio_path = GPIO_PATH % gpio
        except (ValueError, KeyError):
            self.writeerror("Invalid device number")
            return

        if not os.path.isfile(gpio_path):
            self.writeerror("Invalid gpio %s" % gpio_path)
            return

        with open(gpio_path, 'r+') as f:
            value = int(f.readline())
            if value == GPIO_ON:
                self.writeresponse("Power is ON")
            else:
                self.writeresponse("Power is OFF")

        return
