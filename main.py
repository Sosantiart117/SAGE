# Sage
from modulos.Sage import Sage
# Kivy
import kivy
kivy.require('2.0.0')
from kivy.app import App
# from kivy.metrics import dp
# from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager

class SageApp(App):
    """Clase de la app"""
    def build(self):
        return MainLayout()

class MainLayout(FloatLayout):
    pass


class MainBar(BoxLayout):
    title = StringProperty("Tareas")

    def set_title(self,title):
        self.title = title

class SageZone(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

def main():
    Sage.init()
    SageApp().run()

if __name__ == '__main__':
    main()
