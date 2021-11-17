# Sage
from modulos.calendar.calendar_model import Calendar_modelo as calendar_modelo

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
        self.add_widget(MesView())
        self.add_widget(DiaView())
        self.add_widget(Semana())
        self.add_widget(Ao())

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
        self.transition.direction = "down"
        self.current = "Mes"

    def to_dia(self):
        past = self.current
        if past == "Mes":
            self.transition.direction = "up"
        else:
            self.transition.direction = "down"
        self.current = "Dia"

    def to_sem(self):
        past = self.current
        if past == "Año":
            self.transition.direction = "down"
        else:
            self.transition.direction = "up"
        self.current = "Semana"

    def to_ao(self):
        self.transition.direction = "up"
        self.current = "Ao"


class MesView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mes = Mes()
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
        self.mes = Mes(
            year_view=False,
            mes=Calendar.selected_mon,
            year=Calendar.selected_yea,
        )
        self.ids.mes_box.add_widget(self.mes)


class Mes(BoxLayout):
    def __init__(
        self,
        year_view=False,
        mes=Calendar.selected_mon,
        year=Calendar.selected_yea,
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
                week(d_days=days, n_week=i, month=mes, m_days=month_days, year=year)
            )
            days += 7


class day:
    def __init__(self):
        pass


class week(BoxLayout):
    def __init__(self, d_days, n_week, month, m_days, year, **kwargs):
        super().__init__(**kwargs)
        self.spacing = dp(10)
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
        self.add_widget(Button(size_hint=(0.5, 1), text=str(week_label)))
        for i in range(7):
            if days <= 0:
                p_mon = Calendar.get_month(month - 1)[1]
                self.add_widget(Label(text=str(days + p_mon)))
            elif days > m_days:
                self.add_widget(Label(text=str(days - m_days)))
            else:
                self.add_widget(day_button(text=str(days)))
            days += 1


class DiaView(Screen):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    pass


class Dia(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        for i in range(24):
            self.add_widget(Button())

class Semana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bx = BoxLayout()
        for i in range(7):
            bx.add_widget(Dia())
        self.add_widget(bx)

class Ao(Screen):
    def __init__(self,year=Calendar.selected_yea, **kwargs):
        super().__init__(**kwargs)
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
        print(mon)
        pass

    def to_yea(self, yea):
        if not Calendar.selected_yea == int(yea):
            Calendar.selected_yea = int(yea)
            self.show_yea(int(yea))
        pass

    def make_yea(self,year):
        grid = GridLayout(cols=4,rows=3,spacing=dp(10))
        for i in range(12):
            bl = BoxLayout(orientation="vertical")
            bt = Button(text=Calendar.get_month(i+1)[0])
            bt.size_hint = (1, 0.15)
            # bt.bind(on_press=print("hola"))
            bl.add_widget(bt)
            bl.add_widget(Mes(year_view=True, mes=i + 1,year=year))
            grid.add_widget(bl)
        return grid

    def show_yea(self,year):
        self.ids.ao_box.remove_widget(self.yea)
        self.yea=self.make_yea(year)
        self.ids.ao_box.add_widget(self.yea)


class day_button(Button):
    pass
