# window.py
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

from gi.repository import Gtk, Gdk, Gio, GLib
import json
import random

@Gtk.Template(resource_path='/io/github/dida_code/OpstaKultura/window.ui')
class OpstakulturaWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'OpstakulturaWindow'

    zapocni = Gtk.Template.Child()
    skor = Gtk.Template.Child()
    bod = Gtk.Template.Child()
    pitanja = Gtk.Template.Child()
    button1 = Gtk.Template.Child()
    button2 = Gtk.Template.Child()
    button3 = Gtk.Template.Child()
    button4 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Putanja do resursa za questions.json
        bytes = Gio.resources_lookup_data('/io/github/dida_code/OpstaKultura/questions.json', 0)
        res = bytes.get_data().decode("utf-8")

        # Pretvorite JSON string u Python objekt
        self.questions = json.loads(res)

        # Inicijalizacija liste za indekse pitanja
        self.index = []
        self.broj=-1
        self.pitanja.set_text("Da li zelite da zapocnete novu igru?")
        self.zapocni.set_label("Zapocni")
        self.zapocni.connect("clicked", lambda widget: self.prikazi_sledece_pitanje())

    def prikazi_sledece_pitanje(self):
        self.broj = self.broj + 1

        if self.broj < len(self.questions["pitanja"]):
            trenutni_indeks = self.broj
            trenutno_pitanje = self.questions["pitanja"][trenutni_indeks]["pitanje"]
            self.tacan_odgovor = self.questions["pitanja"][trenutni_indeks]["tacan_odgovor"]
            self.trenutni_odgovori = self.questions["pitanja"][trenutni_indeks]["odgovori"]

            print(self.tacan_odgovor)

            self.pitanja.set_text(trenutno_pitanje)
            self.button1.set_label(self.trenutni_odgovori[0])
            self.button2.set_label(self.trenutni_odgovori[1])
            self.button3.set_label(self.trenutni_odgovori[2])
            self.button4.set_label(self.trenutni_odgovori[3])

            # Ponovo vezujte dugmad za funkciju proveri_odgovor
            self.button1.connect("clicked", self.proveri_odgovor)
            self.button2.connect("clicked", self.proveri_odgovor)
            self.button3.connect("clicked", self.proveri_odgovor)
            self.button4.connect("clicked", self.proveri_odgovor)

        else:
            self.pitanja.set_text("Sva pitanja su završena!")
            self.button1.set_label("")
            self.button2.set_label("")
            self.button3.set_label("")
            self.button4.set_label("")

    def proveri_odgovor(self, widget):
        self.button1.disconnect_by_func(self.proveri_odgovor)
        self.button2.disconnect_by_func(self.proveri_odgovor)
        self.button3.disconnect_by_func(self.proveri_odgovor)
        self.button4.disconnect_by_func(self.proveri_odgovor)

        if widget.get_label() == self.tacan_odgovor:
            print("Tacno")

        else:
            print("Netacno")

        self.prikazi_sledece_pitanje()

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Opsta Kultura'
        self.props.version = "0.1.0"
        self.props.authors = ['Dimitrije Kocic']
        self.props.copyright = '2023 Dimitrije Kocic'
        self.set_license_type(Gtk.License.GPL_3_0)
        self.props.logo_icon_name = 'io.github.dida_code.OpstaKultura'
        self.props.modal = True
        self.set_transient_for(parent)
