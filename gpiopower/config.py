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

import configparser

class Config:
    host = ''
    port = 23
    welcome = 'gpiopowerd power control'
    prompt = '> '
    devices = {}

class Device:
    def __init__(self, name, gpio, port):
        self.name = name
        self.gpio = gpio
        self.port = port

def read_config(config_file):
    parser = configparser.ConfigParser()
    parser.read(config_file)
    config = Config()

    if 'host' in parser['DEFAULT']:
        config.host = parser['DEFAULT']['host']

    if 'port' in parser['DEFAULT']:
        config.port = int(parser['DEFAULT']['port'])

    if 'welcome' in parser['DEFAULT']:
        config.welcome = parser['DEFAULT']['welcome']

    if 'prompt' in parser['DEFAULT']:
        config.prompt = parser['DEFAULT']['prompt']

    for device in parser.sections():
        if device == 'DEFAULT':
            continue

        config.devices[int(parser[device]['index'])] = Device(device, int(parser[device]['gpio']), int(parser[device]['port']))

    return config
