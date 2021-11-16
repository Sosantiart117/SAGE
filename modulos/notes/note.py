# Sage
from modulos.notes.note_model import Note_modelo as note_modelo

# kivy (basics)
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

# OPtional (hay que decidir que layouts usar)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout

# Opcional es para usar parametros dentro del .kv
from kivy.properties import StringProperty, BooleanProperty

# Load kv file for Main
Builder.load_file("modulos/notes/note.kv")


class Note(Screen):
    pass


# class TaskZone(Layout):
# pass
