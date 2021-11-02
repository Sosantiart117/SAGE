import sqlite3
from modulos.Sage import Sage

class Task_modelo():

    def __init__(self):
        self.id_task = 0
        self.titulo = "Sin Titulo"
        self.descripcion = ""
        self.estatus = "Registrada"
        self.proy_id = 0
        self.categoria_id = 0
        self.etapa_id = 0
        self.score = 0
        self.path_carpeta= ""
        self.time_creacion = 0
        self.time_inicial = 0
        self.time_final = 0
        self.tipo_task = ""
        
    #insertar en los campos los valores proporcionados
    def summit_task(self): # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        try:
            cur.execute(""" INSERT INTO tasks
            (Titulo, Descripcion, Estatus, Proyecto_Id, Categoria_Id,
            Etapa_Id, Score, Ruta_Carpeta, Fecha_Creacion, Fecha_Inicial, Fecha_Final, Tipo_task)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", self.get_tupla_for_summit())
            db.commit()
            return "Registro exitoso"        
        except sqlite3.Error as err:
            return "Error en la creación del registro"
        finally:
            cur.close()

    #se genera la tupla para insertar los registros
    def get_tupla_for_summit(self):
        info = (self.titulo, self.descripcion, self.estatus, self.proy_id,
         self.categoria_id, self.etapa_id, self.score, self.path_carpeta, self.time_creacion,self.time_inicial,self.time_final, self.tipo_task,)
        return info 

    #se inicializan los valores desde una lista/ tupla de entrada
    def set_valores_individuales(self, lista):
        self.id_task = lista[0]
        self.titulo = lista[1]
        self.descripcion = lista[2]
        self.estatus = lista[3]
        self.proy_id = lista[4]
        self.categoria_id = lista[5]
        self.etapa_id = lista[6]
        self.score = lista[7]
        self.path_carpeta= lista[8]
        self.time_creacion = lista[9]
        self.time_inicial = lista[10]
        self.time_final = lista[11]
        self.tipo_task = lista[12]

    #seleccionar registros con valor en específico.
    @classmethod
    def get_task(cls,  where=None, orden=None):
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        # SObrecarga pytonica
        query = "SELECT * FROM tasks"
        if  where :
            query += " WHERE :where"
        elif orden :
            query += " ORDER BY :order"
        query +=";"
        try:
            cur.execute( query, { "where": where, "order": orden})
            return cur.fetchall()
        except sqlite3.Error as err :
            return  None
        finally:
            cur.close()
