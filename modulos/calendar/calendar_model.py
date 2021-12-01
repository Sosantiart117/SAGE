# sqlite
import sqlite3

#datetime
from datetime import datetime as dt

# Sage
from modulos.Sage import Sage


class Calendar_modelo:
    def __init__(self):
        self.fecha_minima = 0
        self.fecha_maxima=0
    
    def set_fecha_min_día(self,ao, mes, dia, hora):
        self.fecha_minima = dt(ao,mes,dia,hora,0).timestamp()
        return self.fecha_minima

    def set_fecha_max_dia(self,ao, mes, dia, hora):
        self.fecha_maxima = dt(ao,mes,dia,hora,59).timestamp()
        return self.fecha_maxima