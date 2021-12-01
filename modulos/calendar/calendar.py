# Sage
from modulos.calendar.calendar_model import Calendar_modelo as calendar_modelo
from modulos.tasks.task_model import Task_modelo as Task

# kivy (basics)
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

# OPtional (hay que decidir que layouts usar)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# Opcional es para usar parametros dentro del .kv
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.spinner import Spinner

# Python time
import datetime as dt
import math

# Load kv file for Main
Builder.load_file("modulos/calendar/calendar.kv")


class Calendar(Screen):
    selected_day = dt.date.today().day
    selected_mon = dt.date.today().month
    selected_yea = dt.date.today().year
    months = [
        ("Enero", 31),
        ("Febrero", 28),
        ("Marzo", 31),
        ("Abril", 30),
        ("Mayo", 31),
        ("Junio", 30),
        ("Julio", 31),
        ("Agosto", 31),
        ("Septiembre", 30),
        ("Octubre", 31),
        ("Noviembre", 30),
        ("Diciembre", 31),
    ]

    @classmethod
    def get_month(cls, num):
        # Need refactor but
        return Calendar.months[num - 1]

    @classmethod
    def get_day_week(cls, day=1, month=selected_mon, year=selected_yea):
        dia = dt.date(year, month, day).weekday()
        if dia == 6:
            return 1
        else:
            return -dia

    @classmethod
    def get_week(cls, day=1, month=selected_mon, year=selected_yea):
        sem = dt.date(year, month, day).isocalendar()[1]
        if sem > 52:
            return sem - 52
        else:
            return sem



class cal_zone(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mes = MesView(pager=self)
        self.dia = DiaView(pager=self)
        self.sem = Semana(pager=self)
        self.ao = Ao(pager=self)
        self.add_widget(self.mes)
        self.add_widget(self.dia)
        self.add_widget(self.sem)
        self.add_widget(self.ao)

    def move_to(self, where):
        if where == "Mes":
            self.to_mon()
        elif where == "Día":
            self.to_dia()
        elif where == "Semana":
            self.to_sem()
        elif where == "Año":
            self.to_ao()

    def to_mon(self):
        self.mes.show_mon()
        self.transition.direction = "down"
        self.current = "Mes"
        self.parent.parent.ids.view_selector.text = "Mes"

    def to_dia(self):
        self.dia.show_dia()
        past = self.current
        if past == "Mes":
            self.transition.direction = "up"
        else:
            self.transition.direction = "down"
        self.current = "Dia"
        self.parent.parent.ids.view_selector.text = "Dia"

    def to_sem(self):
        # self.sem.show_sem()
        past = self.current
        if past == "Año":
            self.transition.direction = "down"
        else:
            self.transition.direction = "up"
        self.current = "Semana"
        self.parent.parent.ids.view_selector.text = "Semana"

    def to_ao(self):
        self.ao.show_yea(Calendar.selected_yea)
        self.transition.direction = "up"
        self.current = "Ao"
        self.parent.parent.ids.view_selector.text = "Año"

class MesView(Screen):
    def __init__(self, pager=None, **kwargs):
        super().__init__(**kwargs)
        self.pager = pager
        self.mes = Mes(pager=self.pager)
        self.ids.mes_box.add_widget(self.mes)
        self.meses = []
        for i in Calendar.months:
            self.meses.append(i[0])
        self.ids.sel_mon.values = self.meses
        self.ids.sel_mon.text = Calendar.get_month(Calendar.selected_mon)[0]
        yeas = []
        for i in range(1990, 2030):
            yeas.append(str(i))
        self.ids.sel_yea.values = yeas
        self.ids.sel_yea.text = str(Calendar.selected_yea)

    def to_mon(self, month):
        if not Calendar.selected_mon == self.meses.index(month) + 1:
            Calendar.selected_mon = self.meses.index(month) + 1
            self.show_mon()

    def to_yea(self, yea):
        if not Calendar.selected_yea == int(yea):
            Calendar.selected_yea = int(yea)
            self.show_mon()

    def show_mon(self):
        self.ids.mes_box.remove_widget(self.mes)
        self.ids.sel_mon.text = Calendar.get_month(Calendar.selected_mon)[0]
        self.ids.sel_yea.text = str(Calendar.selected_yea)
        self.mes = Mes(
            year_view=False,
            mes=Calendar.selected_mon,
            year=Calendar.selected_yea,
            pager = self.pager
        )
        self.ids.mes_box.add_widget(self.mes)


class Mes(BoxLayout):
    def __init__(
        self,
        year_view=False,
        mes=Calendar.selected_mon,
        year=Calendar.selected_yea,
        pager=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        # Agrega los labels
        bx = BoxLayout(size_hint=(1, 0.1))
        bx.add_widget(Label(text="#. ", size_hint=(0.5, 0.2)))
        labels = ["Dom", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"]
        for i in labels:
            if year_view:
                e = i[0]
            else:
                e = i
            bx.add_widget(Label(text=e, size_hint=(1, 0.2)))
        self.add_widget(bx)

        # Ahora populamos el mes
        # Desfase para que dia empieza el mes
        days = Calendar.get_day_week(month=mes, year=year)
        month_days = Calendar.get_month(mes)[1]
        # Año biciesto
        if mes == 2 and year % 4 == 0:
            month_days = 29
        # para cada semana
        weeks = int(((-days) + month_days) / 7) + 1
        for i in range(weeks):
            self.add_widget(
                week(
                    pager=pager,
                    d_days=days,
                    n_week=i,
                    month=mes,
                    m_days=month_days,
                    year=year,
                )
            )
            days += 7


# clase para guardar los valores de las tasks de un día especifico
class day:
    pass


class horas:
    def __init__(self, ao, mes, dia, hora):
        self.cal_mod = calendar_modelo()
        self.r_minimo = self.cal_mod.set_fecha_min_día(ao, mes, dia, hora)
        self.r_maximo = self.cal_mod.set_fecha_max_dia(ao, mes, dia, hora)


class week(BoxLayout):
    def __init__(self, d_days, n_week, month, m_days, year, pager=None, **kwargs):
        super().__init__(**kwargs)
        self.spacing = dp(10)
        self.pager = pager
        # week button
        days = d_days
        if d_days <= 0:
            s_week = 1
            week_label = Calendar.get_week(day=s_week + 1, month=month, year=year)
        elif d_days >= m_days:
            s_week = d_days
            week_label = Calendar.get_week(day=s_week, month=month, year=year)
            week_label += 1
        else:
            s_week = d_days
            week_label = Calendar.get_week(day=s_week + 1, month=month, year=year)
        wbtn = Button(size_hint=(0.5, 1), text=str(week_label))
        wbtn.bind(on_press=self.to_week)
        self.add_widget(wbtn)
        for i in range(7):
            if days <= 0:
                p_mon = Calendar.get_month(month - 1)[1]
                self.add_widget(Label(text=str(days + p_mon)))
            elif days > m_days:
                self.add_widget(Label(text=str(days - m_days)))
            else:
                db = day_button(ao=year, mes=month, dia=days, text=str(days))
                db.bind(on_press=self.to_day)
                self.add_widget(db)
            days += 1

    def to_day(self, instance):
        Calendar.selected_day = int(instance.text)
        self.pager.to_dia()

    def to_week(self, instance):
        week = int(instance.text)
        self.pager.to_sem()


class DiaView(Screen):
    def __init__(self, pager=None, **kwargs):
        super().__init__(**kwargs)
        self.dia = Dia()
        self.ids.dia_box.add_widget(self.dia)
        self.meses = []
        for i in Calendar.months:
            self.meses.append(i[0])
        self.ids.sel_mon.values = self.meses
        self.ids.sel_mon.text = Calendar.get_month(Calendar.selected_mon)[0]
        yeas = []
        for i in range(1990, 2030):
            yeas.append(str(i))
        self.ids.sel_yea.values = yeas
        self.ids.sel_yea.text = str(Calendar.selected_yea)

        dias = self.get_dias(Calendar.selected_yea, Calendar.selected_mon)
        self.ids.sel_day.values = dias
        self.ids.sel_day.text = str(Calendar.selected_day)

    def to_mon(self, month):
        if not Calendar.selected_mon == self.meses.index(month) + 1:
            Calendar.selected_mon = self.meses.index(month) + 1
            self.show_dia()

    def to_yea(self, yea):
        if not Calendar.selected_yea == int(yea):
            Calendar.selected_yea = int(yea)
            self.show_dia()

    def to_day(self, dia):
        if not Calendar.selected_day == int(dia):
            Calendar.selected_day = int(dia)
            self.show_dia()

    def show_dia(self):
        self.ids.sel_yea.text = str(Calendar.selected_yea)
        self.ids.sel_mon.text = Calendar.get_month(Calendar.selected_mon)[0]
        self.ids.sel_day.text = str(Calendar.selected_day)
        self.ids.dia_box.remove_widget(self.dia)
        self.dia = Dia(
            mes=Calendar.selected_mon,
            year=Calendar.selected_yea,
            day=Calendar.selected_day,
        )
        self.ids.dia_box.add_widget(self.dia)

    def get_dias(self, ao, mes):
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


class Dia(BoxLayout):
    def __init__(
        self,
        pager=None,
        mes=Calendar.selected_mon,
        year=Calendar.selected_yea,
        day=Calendar.selected_day,
        **kwargs
    ):

        super().__init__(**kwargs)
        # Agrega los labels superiores
        bx = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        bx.add_widget(Label(text="Hora", size_hint=(0.3, 0.2)))
        bx.add_widget(Label(text="Tareas", size_hint=(0.5, 0.2)))
        self.add_widget(bx)
        for i in range(24):
            hbx = BoxLayout(orientation="horizontal")
            if i < 10:
                hbx.add_widget(Label(text="0" + str(i), size_hint=(0.1, 0.5)))
            else:
                hbx.add_widget(Label(text=str(i), size_hint=(0.1, 0.5)))
            hbx.add_widget(Hora(year, mes, day, i))
            self.add_widget(hbx)


class Hora(StackLayout):
    def __init__(self, ao, mes, dia, hora, **kwargs):
        super().__init__(**kwargs)
        self.horas = horas(ao, mes, dia, hora)
        self.task = Task()
        registros = self.task.get_task_between(self.horas.r_minimo, self.horas.r_maximo)
        if registros != None:
            for t in registros:
                self.add_widget(task_button(t))
        else:
            self.add_widget(Button(text="Sin tareas", size_hint=(0.9, 0.4)))

    def update(self):
        pass


class Semana(Screen):
    def __init__(self, pager=None, **kwargs):
        super().__init__(**kwargs)
        self.pager = pager
        bx = BoxLayout()
        for i in range(7):
            bx.add_widget(Dia())
        self.add_widget(bx)


class Ao(Screen):
    def __init__(self, year=Calendar.selected_yea, pager=None, **kwargs):
        super().__init__(**kwargs)
        self.pager = pager
        # year selector
        yeas = []
        for i in range(1990, 2030):
            yeas.append(str(i))
        self.ids.sel_yea.values = yeas
        self.ids.sel_yea.text = str(Calendar.selected_yea)
        # Months grid
        self.yea = self.make_yea(year)
        self.ids.ao_box.add_widget(self.yea)

    def to_mon(self, mon):
        # print(mon.mes)
        Calendar.selected_mon = mon.mes
        self.pager.to_mon()
        pass

    def to_yea(self, yea):
        if not Calendar.selected_yea == int(yea):
            Calendar.selected_yea = int(yea)
            self.show_yea(int(yea))
        pass

    def make_yea(self, year):
        self.ids.sel_yea.text = str(year)
        grid = GridLayout(cols=4, rows=3, spacing=dp(10))
        for i in range(12):
            bl = BoxLayout(orientation="vertical")
            bt = ao_m_button(text=Calendar.get_month(i + 1)[0],mes=(i+1))
            bt.size_hint = (1, 0.15)
            bt.bind(on_press=self.to_mon)
            bl.add_widget(bt)
            bl.add_widget(Mes(year_view=True, mes=i + 1, year=year, pager=self.pager))
            grid.add_widget(bl)
        return grid

    def show_yea(self, year):
        self.ids.ao_box.remove_widget(self.yea)
        self.yea = self.make_yea(year)
        self.ids.ao_box.add_widget(self.yea)

class ao_m_button(Button):
    def __init__(self, mes=None,**kwargs):
        super().__init__(**kwargs)
        self.mes = mes


class day_button(Button):
    def __init__(self, ao, mes, dia, **kwargs):
        super().__init__(**kwargs)
        self.ao_dia = ao
        self.mes_dia = mes
        self.dia = dia
        self.cal_mod = calendar_modelo()

    def on_clicked(self):
        Calendar.selected_day = self.dia
        Calendar.selected_mon = self.mes_dia
        Calendar.selected_yea = self.ao_dia


class task_button(Button):
    def __init__(self, tarea, **kwargs):
        super().__init__(**kwargs)
        self.tarea = Task()
        self.tarea = tarea
        self.text = self.tarea.titulo
