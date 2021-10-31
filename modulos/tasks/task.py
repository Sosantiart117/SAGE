# Sage
from modulos.tasks.task_model import Task_modelo as task_modelo
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
        for task in self.get_tasks():
            b = task_button()
            b.set_task(task)
            self.add_widget(b)
        self.add_widget(task_button().set_add())

    def get_tasks(self):
        return task_modelo().get_task()

class task_button(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Extra meta for Buttons
        self.size_hint = (None,None)
        self.size  = (dp(100),dp(100))

    def set_task(self,task_data):
        # Cramos instancia del modelo
        self.task = task_modelo()
        self.task.set_valores_individuales(task_data) 
        self.text = str(self.task.id_task)

    def set_add(self):
        self.text = '+'
        return self
