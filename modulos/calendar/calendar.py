#Sage
from modulos.calendar.calendar_model import Calendar_modelo as calendar_modelo
#kivy (basics)
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
# OPtional (hay que decidir que layouts usar)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
#Opcional es para usar parametros dentro del .kv
from kivy.properties import StringProperty, BooleanProperty

 #Load kv file for Main
Builder.load_file('modulos/calendar/calendar.kv')

class Calendar(Screen):
	contenido = StringProperty("Octubre")
	pass

class cal_zone(ScreenManager):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.add_widget(Mes())
		self.add_widget(Dia())
		self.add_widget(Semana())
		self.add_widget(Ao())
	
	def to_mes(self):
		self.current = "Mes"

	def to_dia(self):
		self.current = "Dia"

	def to_sem(self):
		self.current = "Semana"

	def to_ao(self):
		self.current = "Ao"

class Mes(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)

		days = -3
		month = 32
		for i in range(1,6):
			self.ids.grid.add_widget(
				Button(
					text="w"+str(i),
					size_hint=(.4,1),
					))
			for j in range(1,8):
				if days < 1:
					self.ids.grid.add_widget(Label())
					days+=1
				elif days < month:
					self.ids.grid.add_widget(
					day_button(text=str(days)))
					days += 1

		

class Dia(Screen):
	pass

class Semana(Screen):
	pass

class Ao(Screen):
	pass

class day_button(Button):
	pass