# Sage
from modulos.tasks.task_model import Task_modelo as task_modelo
from modulos.proyects.proyect_model import Proyect_modelo, Categoria_modelo as pro_modelo, cat_modelo
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
        #se inicializan las instancias de las clases para manejar los registros 
        self.task = task_modelo()
        self.proy= pro_modelo()
        self.cat = cat_modelo()
        self.etapa= etapa_modelo()
        self.ids.proy.values = self.get_proy()
        self.ids.tipo.values = self.get_tipos()
        self.ids.etapa.values = self.get_etapas(None)# se quitaría la inicialización
        self.ids.cat.values = self.get_cat(None)     # cuando se implementen los registros
        #variables para las fechas
        self.ids.ao_ini.values= self.get_ao()
        self.ids.hora_ini.values= self.get_hora()
        self.ids.minu_ini.values = self.get_minu()
        self.ids.ao_fin.values = self.get_ao()
        self.ids.hora_fin.values = self.get_hora()
        self.ids.minu_fin.values = self.get_minu()
        self.ao_ini=0
        self.mes_ini=0
        self.dia_ini=0
        self.hora_ini= 0
        self.minu_ini=0
        self.ao_final=0
        self.mes_final=0
        self.dia_final=0
        self.hora_final=0
        self.minu_final=0
        
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
    
    #cuando se seleccionan valores en los spinners
    def spinner_proy_clicked(self, name_proy):
        self.task.proy_id = self.proy.get_id_proy_from_str(nom_proy) # se inicializa el valor del id_proy
        self.ids.cat.values = self.get_cat(self.task.proy_id)

    def spinner_cat_clicked(self, name_cat):
        self.task.categoria_id = self.cat.get_id_cat_from_str(name_cat, self.task.proy_id)
        self.ids.etapa.values = self.get_etapa(self.task.categoria_id)

    def spinner_etapa_clicked(self, name_etapa):
        self.task.etapa_id = self.etapa.get_id_etapa_from_str(name_etapa, self.task.categoria_id) 

    def spinner_tipos_clicked(self, name_tipo):
        self.task.tipo_task = name_tipo          

    def spinner_ao_ini_clicked(self, valor): 
        self.ao_ini = valor
        self.ids.mes_ini.values= self.get_mes()

    def spinner_mes_ini_clicked(self, valor):
        self.mes_ini= valor
        self.ids.dia_ini.values= self.get_dia(self.mes_ini,self.ao_ini)

    def spinner_dia_ini_clicked(self,valor):
        self.dia_ini= valor

    def spinner_hora_ini_clicked(self,valor):
        self.hora_ini= valor

    def spinner_minu_ini_clicked(self,valor):
        self.minu_ini = valor

    def spinner_ao_fin_clicked(self, valor): 
        self.ao_final = valor
        self.ids.mes_fin.values= self.get_mes()

    def spinner_mes_fin_clicked(self, valor):
        self.mes_final= valor
        self.ids.dia_fin.values= self.get_dia(self.mes_final,self.ao_final)

    def spinner_dia_fin_clicked(self,valor):
        self.dia_final= valor

    def spinner_hora_fin_clicked(self,valor):
        self.hora_final= valor

    def spinner_minu_fin_clicked(self,valor):
        self.minu_final = valor

    # De la base de datos cada uno de los modelos
    def get_proy(self):
        #return self.proy.get_titulos_proy()
        return ['SAGE','Por HAver','Escuela']
        pass

    def get_cat(self, id_proy):
        #return self.cat.get_titulos_cat(id_proy)
        return ['Primera','Segunda']
        pass

    def get_etapas(self, id_cat):
        #return self.task.get_titulos_etapa(id_cat)
        return ['UNo','dos']
        pass

    def get_tipos(self):
        return ['Evento','Tarea','Recordatorio']
        pass
        
    def get_ao(self):#para construir las listas de años para el selector de fechas
        lista=[]
        for ao in range(2020,2030):
            lista.append(ao)
        return lista 

    def get_mes(self):#para extraer el mes
        lista=[]
        for mes in range(1,12):
            lista.append(mes)
        return lista

    def get_dia(self, mes, ao):
        lista=[]
        if (mes== 1) or (mes== 3) or  (mes== 5) or  (mes== 7) or (mes== 8) or (mes== 10) or (mes== 12):
            for dia in range(1,31):
                lista.append(dia)
            return lista
        elif (mes==4) or (mes== 6) or (mes== 9) or (mes== 11):
            for dia in range(1,30):
                lista.append(dia)
            return lista
        elif mes == 2:
            for dia in range(1,28):
                lista.append(dia)
            if (ao % 4)==0:
                lista.append(29)
            return lista

    def get_hora(self):
        lista=[]
        for hora in range(0,23):
            lista.append(hora)
        return lista

    def get_minu(self):
        lista=[]
        for minu in range(0,59):
            lista.append(minu)
        return lista

class Views(ScreenManager):

    view = ViewScreen()
    edit = EditScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        task_button.set_pager(self)
        EditScreen.set_zone(self.view.ids.zone)
        self.add_widget(self.view)
        self.add_widget(self.edit)
        
