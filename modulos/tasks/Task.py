# Sage
from modulos.tasks.task_module import Task_Modelo as task_model
# kivy
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('modulos/tasks/task.kv')

class Task(Screen):
    pass

class TaskZone(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = self.get_tasks()
        for task in self.tasks:
            b = task_button()
            b.set_task(task)
            self.add_widget(b)
        self.add_widget(task_button(text='+'))

    def get_tasks(self):
        return task_model().get_task()

class task_button(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Extra meta for Buttons
        self.text = ""
        self.size_hint = (None,None)
        self.size  = (dp(100),dp(100))

    def set_task(self,task_data):
        # Cramos instancia del modelo
        self.task = task_model()
        self.task.set_valores_individuales(task_data) 
        self.text = str(self.task.id_task)

