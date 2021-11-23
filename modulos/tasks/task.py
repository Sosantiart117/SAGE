# Sage
from modulos.tasks.task_model import Task_modelo as task_modelo
from modulos.proyects.proyect_model import (
    Proyect_modelo as pro_modelo,
    Categoria_modelo as cat_modelo,
    Etapa_modelo as etapa_modelo,
)

# datetime
from datetime import datetime

# kivy
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file("modulos/tasks/task.kv")


class Task(Screen):
    pass


class TaskZone(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_tasks()

    def get_tasks(self):
        task = task_modelo().get_task()
        return task

    def show_tasks(self):
        self.clear_widgets()
        try:
            for task in self.get_tasks():
                b = task_button()
                b.set_task(task)
                self.add_widget(b)
        except TypeError:
            print("No hay registros")
        finally:
            self.add_widget(task_button().set_add())


class task_button(Button):
    def set_task(self, task_data):
        # Cramos instancia del modelo
        self.task = task_modelo()
        self.task.set_valores_individuales(task_data)
        texto = self.task.titulo
        if len(texto) > 20:
            texto = texto[:17] + "..."
        self.text = texto

    def set_add(self):
        self.task = None
        self.text = "+"
        return self

    @classmethod
    def set_pager(cls, pager):
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
        self.pager.transition.direction = "left"
        self.pager.current = "edit"


class ViewScreen(Screen):
    # Sorting methods
    print("hola")


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # se inicializan las instancias de las clases para manejar los registros
        self.task = task_modelo()
        self.proy = pro_modelo()
        self.cat = cat_modelo()
        self.etapa = etapa_modelo()
        self.ids.proy.values = self.get_proy()
        self.ids.tipo.values = self.get_tipos()
        self.ids.etapa.values = self.get_etapas("")  # se quitaría la inicialización
        self.ids.cat.values = self.get_cat("")  # cuando se implementen los registros
        # variables para las fechas
        self.ids.ao_ini.values = self.get_ao()
        self.ids.hora_ini.values = self.get_hora()
        self.ids.minu_ini.values = self.get_minu()
        self.ids.ao_fin.values = self.get_ao()
        self.ids.hora_fin.values = self.get_hora()
        self.ids.minu_fin.values = self.get_minu()
        self.ao_ini = 0
        self.mes_ini = 0
        self.dia_ini = 0
        self.hora_ini = 0
        self.minu_ini = 0
        self.ao_final = 0
        self.mes_final = 0
        self.dia_final = 0
        self.hora_final = 0
        self.minu_final = 0

    def set_task(self, task):
        self.task = task

    @classmethod
    def set_zone(cls, zone):
        cls.zone = zone

    def update(self):
        self.ids.desc.text = self.task.descripcion
        self.ids.title.text = self.task.titulo
        self.ids.proy.text = self.proy.get_titulos_proy(self.task.proy_id)
        self.ids.tipo.text = self.task.tipo_task
        self.ids.cat.text = self.cat.get_titulos_cat(0, self.task.categoria_id)
        self.ids.etapa.text = self.etapa.get_titulos_etapa(0, self.task.etapa_id)
        self.setFechas_ini(self.task.time_inicial)
        self.setFechas_fin(self.task.time_final)

    def save(self):
        # Save to DB
        self.task.titulo = self.ids.title.text
        self.task.descripcion = self.ids.desc.text
        self.task.estatus = "Agregada"
        # Falta implementar la forma de tomar el int
        # self.task.proy_id = 0
        # self.task.categoria_id = 0
        # self.task.etapa_id = 0
        fecha_i = self.getFechasSegundos(
            self.ao_ini, self.mes_ini, self.dia_ini, self.hora_ini, self.minu_ini
        )
        fecha_f = self.getFechasSegundos(
            self.ao_final,
            self.mes_final,
            self.dia_final,
            self.hora_final,
            self.minu_final,
        )
        if fecha_i < fecha_f:
            # self.task.time_inicial = fecha_i
            # self.task.time_final = fecha_f
            if (
                self.task.id_task != 0
            ):  # para identificar si se crea registro o se modifica el existente
                # self.task.update_task()
                alerta = Popup(
                    title="Modificación de registro",
                    content=Label(text="Se modificó el registro exitosamente."),
                    size_hint=(None, None),
                    size=(400, 400),
                )
                alerta.open()
            else:
                # self.task.time_creacion = int(datetime.now().timestamp())
                # self.task.summit_task()
                alerta = Popup(
                    title="Inserción de registro",
                    content=Label(text="Se insertó el registro exitosamente."),
                    size_hint=(None, None),
                    size=(400, 400),
                )
                alerta.open()
            self.zone.show_tasks()
            # Back to view
            self.parent.transition.direction = "right"
            self.parent.current = "view"
        else:
            alerta = Popup(
                title="Error al registrar",
                content=Label(text="Fechas inválidas."),
                size_hint=(None, None),
                size=(400, 400),
            )
            alerta.open()

    def quit(self):
        # Tira la info
        # Back to view
        self.parent.transition.direction = "right"
        self.parent.current = "view"

    # cuando se seleccionan valores en los spinners
    def spinner_proy_clicked(self, name_proy):
        self.task.proy_id = self.proy.get_id_proy_from_str(
            nom_proy
        )  # se inicializa el valor del id_proy
        self.ids.cat.values = self.get_cat(self.task.proy_id)

    def spinner_cat_clicked(self, name_cat):
        self.task.categoria_id = self.cat.get_id_cat_from_str(
            name_cat, self.task.proy_id
        )
        self.ids.etapa.values = self.get_etapa(self.task.categoria_id)

    def spinner_etapa_clicked(self, name_etapa):
        self.task.etapa_id = self.etapa.get_id_etapa_from_str(
            name_etapa, self.task.categoria_id
        )

    def spinner_tipos_clicked(self, name_tipo):
        self.task.tipo_task = name_tipo

    def spinner_ao_ini_clicked(self, valor):
        self.ao_ini = int(valor)
        self.ids.mes_ini.values = self.get_mes()

    def spinner_mes_ini_clicked(self, valor):
        self.mes_ini = int(valor)
        self.ids.dia_ini.values = self.get_dia(self.mes_ini, self.ao_ini)

    def spinner_dia_ini_clicked(self, valor):
        self.dia_ini = int(valor)

    def spinner_hora_ini_clicked(self, valor):
        self.hora_ini = int(valor)

    def spinner_minu_ini_clicked(self, valor):
        self.minu_ini = int(valor)

    def spinner_ao_fin_clicked(self, valor):
        self.ao_final = int(valor)
        self.ids.mes_fin.values = self.get_mes()

    def spinner_mes_fin_clicked(self, valor):
        self.mes_final = int(valor)
        self.ids.dia_fin.values = self.get_dia(self.mes_final, self.ao_final)

    def spinner_dia_fin_clicked(self, valor):
        self.dia_final = int(valor)

    def spinner_hora_fin_clicked(self, valor):
        self.hora_final = int(valor)

    def spinner_minu_fin_clicked(self, valor):
        self.minu_final = int(valor)

    # De la base de datos cada uno de los modelos
    def get_proy(self):
        # return self.proy.get_titulos_proy()
        return ["SAGE", "Por HAver", "Escuela"]
        pass

    def get_cat(self, id_proy):
        # return self.cat.get_titulos_cat(id_proy)
        return ["Primera", "Segunda"]
        pass

    def get_etapas(self, id_cat):
        # return self.task.get_titulos_etapa(id_cat)
        return ["UNo", "dos"]
        pass

    def get_tipos(self):
        return ["Evento", "Tarea", "Recordatorio"]
        pass

    def get_ao(self):  # para construir las listas de años para el selector de fechas
        lista = []
        for ao in range(2020, 2031):
            lista.append(str(ao))
        return lista

    def get_mes(self):  # para extraer el mes
        lista = []
        for mes in range(1, 13):
            if mes < 10:
                lista.append("0" + str(mes))
            else:
                lista.append(str(mes))
        return lista

    def get_dia(self, mes, ao):
        lista = []
        if (
            (mes == 1)
            or (mes == 3)
            or (mes == 5)
            or (mes == 7)
            or (mes == 8)
            or (mes == 10)
            or (mes == 12)
        ):
            for dia in range(1, 32):
                if dia < 10:
                    lista.append("0" + str(dia))
                else:
                    lista.append(str(dia))
            return lista
        elif (mes == 4) or (mes == 6) or (mes == 9) or (mes == 11):
            for dia in range(1, 31):
                if dia < 10:
                    lista.append("0" + str(dia))
                else:
                    lista.append(str(dia))
            return lista
        elif mes == 2:
            for dia in range(1, 29):
                if dia < 10:
                    lista.append("0" + str(dia))
                else:
                    lista.append(str(dia))
            if (ao % 4) == 0:
                lista.append(str(29))
            return lista

    def get_hora(self):
        lista = []
        for hora in range(0, 24):
            if hora < 10:
                lista.append("0" + str(hora))
            else:
                lista.append(str(hora))
        return lista

    def get_minu(self):
        lista = []
        for minu in range(0, 60):
            if minu < 10:
                lista.append("0" + str(minu))
            else:
                lista.append(str(minu))
        return lista

    def getFechasSegundos(self, año, mes, dia, hora, minuto):
        fecha = datetime(año, mes, dia, hora, minuto, 0).timestamp()
        return int(fecha)

    # para extraer el timestamp de las fechas para task generadas en el editor
    def setFechas_ini(self, fechaTimestamp):
        if fechaTimestamp != 0:
            fecha = datetime.fromtimestamp(fechaTimestamp)
            self.ao_ini = fecha.year
            self.ids.ao_ini.text = str(self.ao_ini)
            self.mes_ini = fecha.month
            if self.mes_ini < 10:
                self.ids.mes_ini.text = "0" + str(self.mes_ini)
            else:
                self.ids.mes_ini.text = str(self.mes_ini)
            self.dia_ini = fecha.day
            if self.dia_ini < 10:
                self.ids.dia_ini.text = "0" + str(self.dia_ini)
            else:
                self.ids.dia_ini.text = str(self.dia_ini)
            self.hora_ini = fecha.hour
            if self.hora_ini < 10:
                self.ids.hora_ini.text = "0" + str(self.hora_ini)
            else:
                self.ids.hora_ini.text = str(self.hora_ini)
            self.minu_ini = fecha.minute
            if self.minu_ini < 10:
                self.ids.minu_ini.text = "0" + str(self.minu_ini)
            else:
                self.ids.minu_ini.text = str(self.minu_ini)

    def setFechas_fin(self, fechaTimestamp):
        if fechaTimestamp != 0:
            fecha = datetime.fromtimestamp(fechaTimestamp)
            self.ao_final = fecha.year
            self.ids.ao_fin.text = str(self.ao_final)
            self.mes_final = fecha.month
            if self.mes_final < 10:
                self.ids.mes_fin.text = "0" + str(self.mes_final)
            else:
                self.ids.mes_fin.text = str(self.mes_final)
            self.dia_final = fecha.day
            if self.dia_final < 10:
                self.ids.dia_fin.text = "0" + str(self.dia_final)
            else:
                self.ids.dia_fin.text = str(self.dia_final)
            self.hora_final = fecha.hour
            if self.hora_final < 10:
                self.ids.hora_fin.text = "0" + str(self.hora_final)
            else:
                self.ids.hora_fin.text = str(self.hora_final)
            self.minu_final = fecha.minute
            if self.minu_final < 10:
                self.ids.minu_fin.text = "0" + str(self.minu_final)
            else:
                self.ids.minu_fin.text = str(self.minu_final)


class Views(ScreenManager):

    view = ViewScreen()
    edit = EditScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        task_button.set_pager(self)
        EditScreen.set_zone(self.view.ids.zone)
        self.add_widget(self.view)
        self.add_widget(self.edit)
