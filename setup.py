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

"""gpiopowerd setup script"""

from setuptools import setup
import versioneer

setup(
    name='gpiopowerd',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='GPIO powerd',
    long_description='',

    url='https://github.com/mjeanson/gpiopowerd',

    author='Michael Jeanson',
    author_email='mjeanson@efficios.com',

    license='MIT',

    packages=[
        'gpiopowerd',
        ],

    entry_points={
        'console_scripts': [
            'gpio-powerd = gpiopowerd:run',
        ],
    },

    extras_require={
        'telnetsrv':  ["telnetsrv"]
    },
)