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

from os import path

GPIO_PATH = '/sys/class/gpio/gpio%d'
EXPORT_PATH = '/sys/class/gpio/export'

def config_gpio(gpio):
    gpio_path = GPIO_PATH % gpio

    if not path.isdir(gpio_path):
        with open(EXPORT_PATH, 'r+') as f:
            f.write(str(gpio))
            f.flush()

    with open(path.join(gpio_path, 'direction'), 'r+') as f:
        f.write('high')
        f.flush()

    with open(path.join(gpio_path, 'active_low'), 'r+') as f:
        f.write('1')
        f.flush()

def config_gpios(config):
    for (k, v) in config.devices.items():
        config_gpio(v.gpio)
