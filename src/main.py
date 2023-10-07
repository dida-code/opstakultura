# main.py
#
# Copyright 2023 Dimitrije Kocic
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import OpstakulturaWindow


class OpstakulturaApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.dida_code.OpstaKultura',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('zatvori', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('nova', self.on_nova_action)

    def quit(self, action, parameter):
        self.get_active_window().close()

    def on_nova_action(self, widget, *args):
        win = self.props.active_window
        if win and hasattr(win, 'nova') and callable(getattr(win, 'nova')):
            win.nova()
        else:
            # Ako prozor nije aktivan ili nema 'nova' metode, otvorite novi prozor
            win = OpstakulturaWindow(application=self)



    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = OpstakulturaWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Opsta Kultura',
                                application_icon='io.github.dida_code.OpstaKultura',
                                developer_name='Dimitrije Kocic',
                                version='1.1.1',
                                developers=['Dimitrije Kocic'],
                                website='https://github.com/dida-code/opstakultura',
                                copyright='© 2023 Dimitrije Kocic',
                                license_type=Gtk.License.GPL_3_0)
        about.present()



    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = OpstakulturaApplication()
    return app.run(sys.argv)
