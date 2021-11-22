# Sage
from modulos.proyects.proyect_model import Proyect_modelo as proyect_modelo

# kivy (basics)
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

# OPtional (hay que decidir que layouts usar)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout

# Opcional es para usar parametros dentro del .kv
from kivy.properties import StringProperty, BooleanProperty

# Load kv file for Main
Builder.load_file("modulos/proyects/proyect.kv")


class Proyect(Screen):
    pass


class ProyectZone(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_proyects()

    def get_proys(self):
        pass

    def show_proyects(self):
        self.clear_widgets()
        try:
            for proy in self.get_proys():
                b = proy_button()
                b.set_proy(proy)
                self.add_widget(b)
        except TypeError:
            print("No hay registros")
        finally:
            self.add_widget(proy_button().set_add())


class proy_button(Button):
    def set_proy(self, proy_data):
        pass

    def set_add(self):
        self.text = "+"
        return self

    def to_etap(self):
        root = self.parent.parent.parent.parent.parent
        root.curret = 'etapa'
        pass

    def edit(self):
        pass

class etap_button(Button):
    def set_etap(self, etap_data):
        pass


    def set_add(self):
        self.text = "+"
        return self

    def edit(self):
        pass


class ProyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

class EtapaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class Views(ScreenManager):

    proy = ProyScreen()
    etap = EtapaScreen()
    edit = EditScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
