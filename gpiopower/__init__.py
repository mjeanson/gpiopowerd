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

import argparse
import logging

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .handler import GPIOPowerHandler
from .server import GPIOPowerServer
from .config import read_config
from .gpio import config_gpios

logging.getLogger('').setLevel(logging.DEBUG)

def daemon():
    parser = argparse.ArgumentParser( description='Run a telnet server.')
    parser.add_argument( '-c', '--conf', metavar="CONFIG", type=str, help="The path to the config file.", required=True)
    args = parser.parse_args()
    config = read_config(args.conf)

    server = GPIOPowerServer(config, GPIOPowerHandler)

    config_gpios(config)

    logging.info("Starting gpiopowerd at port %d.  (Ctrl-C to stop)" % config.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server shut down.")
