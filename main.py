# Sage
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from modulos.Sage import Sage
from modulos.tasks.task import Task
from modulos.notes.note import Note
from modulos.calendar.calendar import Calendar
from modulos.proyects.proyect import Proyect


# Kivy
import kivy 


kivy.require("2.0.0")
from kivy.app import App

# from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition

class SageApp(App):
    """Clase de la app"""

    def build(self):
        return Main()


class Main(FloatLayout):
    pass

class Bar(BoxLayout):
    title = StringProperty("Tareas")

    def set_title(self, title):
        self.title = title

    def to_start(self):
        root = self.parent.ids.main_pager
        root.transition.direction = 'right'
        root.current = "start"


class MainPager(ScreenManager):
    pass

class Profile(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'

class Start(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(StartLayout())
        self.name = 'start'

class StartLayout(FloatLayout):
    def to_main(self,where):
        root = self.parent.parent
        zone = root.ids.main.ids.main.ids.zone
        zone.current = where
        root.transition.direction = 'left'
        root.current = 'main'

class MainScreen(Screen):
    pass

class MainLayout(FloatLayout):
    pass

class SageZone(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Task())
        self.add_widget(Calendar())
        self.add_widget(Note())
        self.add_widget(Proyect())


class Navmenu(BoxLayout):
    # def __init__(self,**kwargs):
    #     super().__init__(**kwargs)
    #     # self.zone = self.parent.ids.zone
    #     # print(self.parent)
    #     # print(self.parent.ids)

    def to_task(self):
        zone = self.parent.parent.ids.zone
        window = zone.current
        if not window == "Tasks":
            zone.transition.direction = "down"
            zone.current = "Tasks"

    def to_cal(self):
        zone = self.parent.parent.ids.zone
        window = zone.current
        if window == "Calendar":
            pass
        elif window == "Tasks":
            zone.transition.direction = "up"
            zone.current = "Calendar"
        else:
            zone.transition.direction = "down"
            zone.current = "Calendar"

    def to_notes(self):
        zone = self.parent.parent.ids.zone
        window = zone.current
        if window == "Notes":
            pass
        elif window == "Proyects":
            zone.transition.direction = "down"
            zone.current = "Notes"
        else:
            zone.transition.direction = "up"
            zone.current = "Notes"

    def to_proyectos(self):
        zone = self.parent.parent.ids.zone
        window = zone.current
        if not window == "Proyects":
            zone.transition.direction = "up"
            zone.current = "Proyects"


def main():
    Sage.init()
    SageApp().run()


if __name__ == "__main__":
    main()
