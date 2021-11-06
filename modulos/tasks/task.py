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
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file('modulos/tasks/task.kv')

class Task(Screen):
    pass

class TaskZone(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_tasks()

    def get_tasks(self):
        return task_modelo().get_task()

    def show_tasks(self):
        self.clear_widgets()
        for task in self.get_tasks():
            b = task_button()
            b.set_task(task)
            self.add_widget(b)
        self.add_widget(task_button().set_add())

class task_button(Button):
    def set_task(self,task_data):
        # Cramos instancia del modelo
        self.task = task_modelo()
        self.task.set_valores_individuales(task_data) 
        texto = self.task.titulo
        if len(texto) > 20:
            texto = texto[:17] + "..."
        self.text = texto

    def set_add(self):
        self.task = None
        self.text = '+'
        return self

    @classmethod
    def set_pager(cls,pager):
        cls.pager = pager

    def edit(self):
        # Give edit information for edit panel
        if self.task == None:
            # New Task
            self.pager.edit.set_task(task_modelo())
        else:
            # Existing task
            self.pager.edit.set_task(self.task)
        self.pager.edit.update()
        # Show edit panel
        self.pager.transition.direction = 'left'
        self.pager.current = 'edit'

class ViewScreen(Screen):
    # Sorting methods
    def click(self):
        print("hola")

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task = task_modelo()
        self.ids.proy.values = self.get_proy()
        self.ids.tipo.values = self.get_tipos()
        self.ids.etapa.values = self.get_etapas()
        self.ids.cat.values = self.get_cat()
        
    def set_task(self, task):
        self.task = task

    @classmethod
    def set_zone(cls, zone):
        cls.zone = zone

    def update(self):
        self.ids.desc.text = self.task.descripcion
        self.ids.title.text = self.task.titulo

    def save(self):
        # Save to DB
        self.task.titulo = self.ids.title.text
        self.task.descripcion = self.ids.desc.text
        self.task.estatus = "Agregada"
        # Falta implementar la forma de tomar el int
        # self.task.proy_id = 0
        # self.task.categoria_id = 0
        # self.task.etapa_id = 0
        # self.task.time_creacion = 0
        # self.task.time_inicial = 0
        # self.task.time_final = 0
        # self.task.tipo_task = ""
        
        if self.task.id_task!= 0:#para identificar si se crea registro o se modifica el existente
            self.task.update_task()
        else:
            self.task.summit_task()
            
        self.zone.show_tasks()
        # Back to view
        self.parent.transition.direction = 'right'
        self.parent.current = 'view'


    def quit(self):
        # Tira la info
        # Back to view
        self.parent.transition.direction = 'right'
        self.parent.current = 'view'


    # De la base de datos cada uno de los modelos
    def get_proy(self):
        return ['SAGE','Por HAver','Escuela']
        pass

    def get_cat(self):
        return ['Primera','Segunda']
        pass

    def get_etapas(self):
        return ['UNo','dos']
        pass

    def get_tipos(self):
        return ['UNo','dos']
        pass

class Views(ScreenManager):

    view = ViewScreen()
    edit = EditScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        task_button.set_pager(self)
        EditScreen.set_zone(self.view.ids.zone)
        self.add_widget(self.view)
        self.add_widget(self.edit)
        
