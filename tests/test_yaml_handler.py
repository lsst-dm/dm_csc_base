# This file is part of dm_csc_base
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asynctest
from datetime import time

from lsst.dm.csc.base.YamlHandler import YamlHandler


class YamlHandlerTestCase(asynctest.TestCase):

    def test_encode_decode(self):
        handler = YamlHandler(None)

        d = {"foo1": "bar1", "foo2": "bar2"}

        s = handler.encode_message(d)
        self.assertEqual(s, 'foo1: bar1\nfoo2: bar2\n')

        m = handler.decode_message(s)
        self.assertEqual(m["foo1"], "bar1")
        self.assertEqual(m["foo2"], "bar2")

    def test_datetime(self):
        handler = YamlHandler()
        d = {"date": time(hour=9, minute=27, second=55)}

        s = handler.encode_message(d)
        m = handler.decode_message(s)

        d2 = m["date"]
        self.assertEqual(d2.hour, 9)
        self.assertEqual(d2.minute, 27)
        self.assertEqual(d2.second, 55)

    def test_callback(self):
        handler = YamlHandler(self.on_message)

        d = {"foo1": "bar1", "foo2": "bar2"}

        s = handler.encode_message(d)
        self.assertEqual(s, 'foo1: bar1\nfoo2: bar2\n')

        handler.yaml_callback(None, None, None, s)

    def on_message(self, channel, basic_deliver, properties, body):
        self.assertEqual(body["foo1"], "bar1")
        self.assertEqual(body["foo2"], "bar2")
