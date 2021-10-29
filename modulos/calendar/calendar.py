#Sage
from modulos.calendar.calendar_model import Calendar_modelo as calendar_modelo
#kivy (basics)
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
# OPtional (hay que decidir que layouts usar)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
#Opcional es para usar parametros dentro del .kv
from kivy.properties import StringProperty, BooleanProperty

 #Load kv file for Main
Builder.load_file('modulos/calendar/calendar.kv')

class Calendar(Screen):
	pass

#class TaskZone(Layout):
	#pass
