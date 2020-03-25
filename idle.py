#!/usr/bin/env python

import sys
import dbus
import requests
import datetime
import dbus.mainloop.glib
from gi.repository import GLib


class Idle:

    last = datetime.datetime.now()

    def active_changed(self, status):
        now = datetime.datetime.now()
        diff = (now - self.last).total_seconds()
        self.last = now
        print(diff)
        print(status)
        if status:
            requests.get('http://ir-blaster/off')
        else:
            if diff < 33 or diff > 35:
                requests.get('http://ir-blaster/on')

    def process(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        bus = dbus.SessionBus()
        obj = bus.get_object("org.gnome.ScreenSaver","/org/gnome/ScreenSaver")
        obj.connect_to_signal("ActiveChanged", self.active_changed, dbus_interface="org.gnome.ScreenSaver")

        loop = GLib.MainLoop()
        loop.run()


if __name__ == '__main__':
    Idle().process()
