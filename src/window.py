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

from gi.repository import Gtk, Gdk, Gio, GLib, Pango
import json
import random

@Gtk.Template(resource_path='/io/github/dida_code/OpstaKultura/window.ui')
class OpstakulturaWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'OpstakulturaWindow'
    
    
    box = Gtk.Template.Child()
    box_dugme = Gtk.Template.Child()
    tq = Gtk.Template.Child()
    zapocni = Gtk.Template.Child()
    skor = Gtk.Template.Child()
    pitanja = Gtk.Template.Child()
    button1 = Gtk.Template.Child()
    button2 = Gtk.Template.Child()
    button3 = Gtk.Template.Child()
    button4 = Gtk.Template.Child()
    broj_pitanja = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.skor.hide()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.broj_pitanja.hide()
        self.tq.hide()
        
        
        self.box_dugme.get_style_context().add_class("box2")
        self.box.get_style_context().add_class("box")
        self.skor.get_style_context().add_class("skor")
        self.zapocni.get_style_context().add_class("button")
        self.pitanja.get_style_context().add_class("pitanja")
        self.button1.get_style_context().add_class("button")
        self.button2.get_style_context().add_class("button")
        self.button3.get_style_context().add_class("button")
        self.button4.get_style_context().add_class("button")
        self.broj_pitanja.get_style_context().add_class("skor")
        self.tq.get_style_context().add_class("skor")
        
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path('style.css'))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Putanja do resursa za questions.json
        bytes = Gio.resources_lookup_data('/io/github/dida_code/OpstaKultura/questions.json', 0)
        res = bytes.get_data().decode("utf-8")

        # Pretvorite JSON string u Python objekt
        self.questions = json.loads(res)

        # Inicijalizacija liste za indekse pitanja
        self.index = []
        self.broj=-1
        self.poen=0
        self.pracenje_pitanja = 0
        self.pitanja.set_text("Do you want to start a new game?")
        self.zapocni.set_label("Start")
        random.shuffle(self.questions["pitanja"])
        self.zapocni.connect("clicked", lambda widget: self.prikazi_sledece_pitanje())

    def prikazi_sledece_pitanje(self):
        ukupno_pitanja=len(self.questions["pitanja"])
        self.tq.set_label(f"Total Questions\n{ukupno_pitanja}")
        self.skor.set_label(f"Score: {self.poen}")
        self.tq.show()
        self.skor.show()
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.button4.show()
        self.zapocni.hide()
        self.broj = self.broj + 1
        print(self.pracenje_pitanja)
        if self.pracenje_pitanja < 40:
            self.pracenje_pitanja += 1 
            self.broj_pitanja.set_label(f'Question {self.pracenje_pitanja}/40')
        self.broj_pitanja.show()

        if self.broj < 40:
            trenutni_indeks = self.broj
            trenutno_pitanje = self.questions["pitanja"][trenutni_indeks]["pitanje"]
            self.tacan_odgovor = self.questions["pitanja"][trenutni_indeks]["tacan_odgovor"]
            self.trenutni_odgovori = self.questions["pitanja"][trenutni_indeks]["odgovori"]
            random.shuffle(self.trenutni_odgovori)
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
            self.pitanja.set_text(f"All questions completed!\n Your score is {self.poen}!\n Do you want to start a new game?")
            self.zapocni.show()
            random.shuffle(self.questions["pitanja"])
            self.zapocni.connect("clicked", lambda widget: self.restart())
            self.broj=-1
            self.poen=0
            self.pracenje_pitanja = 0
            self.button1.hide()
            self.button2.hide()
            self.button3.hide()
            self.button4.hide()

    def restart(self):
        pass

    def nova (self):
        if self.pracenje_pitanja == 0:
            pass

        else:
            self.broj=0
            self.poen=0
            self.pracenje_pitanja = 1
            self.skor.set_label(f"Score: {self.poen}")
            self.broj_pitanja.set_label(f'Question {self.pracenje_pitanja}/{len(self.questions["pitanja"])}')
            random.shuffle(self.questions["pitanja"])
            trenutni_indeks = self.broj
            trenutno_pitanje = self.questions["pitanja"][trenutni_indeks]["pitanje"]
            self.tacan_odgovor = self.questions["pitanja"][trenutni_indeks]["tacan_odgovor"]
            self.trenutni_odgovori = self.questions["pitanja"][trenutni_indeks]["odgovori"]
            random.shuffle(self.trenutni_odgovori)
            self.pitanja.set_text(trenutno_pitanje)
            self.button1.set_label(self.trenutni_odgovori[0])
            self.button2.set_label(self.trenutni_odgovori[1])
            self.button3.set_label(self.trenutni_odgovori[2])
            self.button4.set_label(self.trenutni_odgovori[3])



    def proveri_odgovor(self, widget):
        self.button1.disconnect_by_func(self.proveri_odgovor)
        self.button2.disconnect_by_func(self.proveri_odgovor)
        self.button3.disconnect_by_func(self.proveri_odgovor)
        self.button4.disconnect_by_func(self.proveri_odgovor)

        if widget.get_label() == self.tacan_odgovor:
            self.poen +=1

        else:
            pass

        self.prikazi_sledece_pitanje()
