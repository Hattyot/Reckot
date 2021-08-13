import gi
import os

gi.require_version('Vte', '2.91')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte, GLib, Gdk

window_size_x = 800
window_size_y = 300


class Reckot(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_decorated(False)  # remove all window interactivity like size adjustment
        self.set_default_size(window_size_x, window_size_y)

        display = Gdk.Display.get_default()
        seat = display.get_default_seat()
        pointer = seat.get_pointer()

        _, pointer_x, pointer_y = (pointer.get_position())

        monitor = display.get_monitor_at_point(pointer_x, pointer_y)
        window_geometry = monitor.get_geometry()
        x, y = ((window_geometry.width - window_size_x) // 2) + window_geometry.x, 0

        self.move(x, y)

        self.terminal = Vte.Terminal()
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1
        )

        self.window = Gtk.ScrolledWindow()
        self.window.set_hexpand(True)
        self.window.add(self.terminal)

        self.box = Gtk.Box()
        self.box.pack_start(self.window, False, True, 0)

        self.add(self.box)


def main():
    reckot = Reckot()
    # close process on window close
    reckot.connect("delete-event", Gtk.main_quit)
    reckot.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
