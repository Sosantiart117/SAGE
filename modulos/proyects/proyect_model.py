# sqlite
import sqlite3

# Sage
from modulos.Sage import Sage


class Proyect_modelo:
    def __init__(self):
        # definimos las variables necesarias de la tabla proyectos
        self.id_proy = 0
        self.name_proy = ""
        self.desc_proy = ""
        self.status_proy = ""
        self.path_proy = ""
        self.time_crea_proy = 0
        pass

    # insertar en los campos los valores proporcionados
    def summit_proy(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        # cambio por generar scripts para registrar valores numéricos
        script = """ INSERT INTO "proyectos"
            (Titulo, Descripcion, Estatus, Ruta_Carpeta, Fecha_Creacion)
            VALUES ('{}', '{}', '{}', '{}', {});""".format(
            self.get_tupla_for_summit()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Registro exitoso"
        except sqlite3.Error as err:
            return "Error en la creación del registro"
        finally:
            cur.close()

    # se genera la tupla para insertar los registros
    def get_tupla_for_summit(self):
        info = (
            self.name_proy,
            self.desc_proy,
            self.status_proy,
            self.path_proy,
            self.time_crea_proy,
        )
        return info

    # se genera la tupla para modificar los registros existentes
    def get_tupla_for_update(self):
        info = (
            self.name_proy,
            self.desc_proy,
            self.status_proy,
            self.path_proy,
            self.time_crea_proy,
            self.id_proy,
        )  # se agrega el id_proy al final como parametro del where
        return info

    # Se realizan las updates a los registros
    def update_proy(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ UPDATE "proyectos"
            SET Titulo= '{}', Descripcion= '{}', Estatus= '{}',  Ruta_Carpeta = '{}',
             Fecha_Creacion = {} WHERE Id_proyecto= {} ;""".format(
            self.get_tupla_for_update()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Modificación exitoso"
        except sqlite3.Error as err:
            return "Error en la modificación del registro"
        finally:
            cur.close()

    # los getters para obtener los nombres y el id de los proyectos
    def get_titulos_proy(
        self,
    ):  # Retorna los titulos de los proyectos para los spinners
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ SELECT Titulo FROM "proyectos" ORDER BY Id_proyecto ;"""
        try:
            cur.execute(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()

    def get_id_proy_from_str(self, nom_proy):
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """SELECT Id_proyecto FROM "proyectos" WHERE Titulo = '{}' ;""".format(
            nom_proy
        )
        try:
            cur.executescript(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()


class Categoria_modelo:  # se crea la clase categorías para las interacciones con la tabla en la DB
    def __init__(self):
        self.id_cat = 0
        self.name_cat = ""
        self.desc_cat = ""
        self.status_cat = ""
        self.proy_id_cat = 0
        self.path_cat = ""
        self.time_crea_etapa = 0
        pass

    # insertar en los campos los valores proporcionados
    def summit_cat(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        # cambio por generar scripts para registrar valores numéricos
        script = """ INSERT INTO "categorias"
            (Titulo, Descripcion, Estatus, Proyecto_Id, Ruta_Carpeta, Fecha_Creacion)
            VALUES ('{}', '{}', '{}', {}, '{}', {});""".format(
            self.get_tupla_for_summit()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Registro exitoso"
        except sqlite3.Error as err:
            return "Error en la creación del registro"
        finally:
            cur.close()

    # se genera la tupla para insertar los registros
    def get_tupla_for_summit(self):
        info = (
            self.name_cat,
            self.desc_cat,
            self.status_cat,
            self.proy_id_cat,
            self.path_cat,
            self.time_crea_cat,
        )
        return info

    # se genera la tupla para modificar los registros existentes
    def get_tupla_for_update(self):
        info = (
            self.name_cat,
            self.desc_cat,
            self.status_cat,
            self.proy_id_cat,
            self.path_cat,
            self.time_crea_cat,
            self.id_cat,
        )  # se agrega el id_cat al final como parametro del where
        return info

    # Se realizan las updates a los registros
    def update_cat(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ UPDATE "categorias"
            SET Titulo= '{}', Descripcion= '{}', Estatus= '{}', Proyecto_Id= {},  Ruta_Carpeta = '{}',
             Fecha_Creacion = {} WHERE Id_categorias= {} ;""".format(
            self.get_tupla_for_update()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Modificación exitoso"
        except sqlite3.Error as err:
            return "Error en la modificación del registro"
        finally:
            cur.close()

    # los getters para obtener los nombres y el id de las categorías
    def get_titulos_cat(
        self, id_proy
    ):  # Retorna los titulos de las categorías para los spinners
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ SELECT Titulo FROM "categorias" WHERE Proyecto_Id = {} ORDER BY Id_categorias ;""".format(
            id_proy
        )
        try:
            cur.execute(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()

    def get_id_cat_from_str(self, nom_cat, id_proy):
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """SELECT Id_categorias FROM "categorias" WHERE Titulo = '{}' AND Proyecto_Id= {} ;""".format(
            nom_cat, id_proy
        )
        try:
            cur.executescript(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()


class Etapa_modelo:  # se crea la clase categorías para las interacciones con la tabla en la DB
    def __init__(self):
        self.id_etapa = 0
        self.name_etapa = ""
        # self.status_etapa="" #no sé porque no hay status, todo meco el compañero que lo hizo xd
        self.cat_id_etapa = ""
        self.path_etapa = ""
        self.time_crea_etapa = 0
        pass

    # insertar en los campos los valores proporcionados
    def summit_etapa(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        # cambio por generar scripts para registrar valores numéricos
        script = """ INSERT INTO "etapas"
            (Titulo, Categoria_Id, Ruta_Carpeta, Fecha_Creacion)
            VALUES ('{}', {}, '{}', {});""".format(
            self.get_tupla_for_summit()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Registro exitoso"
        except sqlite3.Error as err:
            return "Error en la creación del registro"
        finally:
            cur.close()

    # se genera la tupla para insertar los registros
    def get_tupla_for_summit(self):
        info = (
            self.name_etapa,
            self.cat_id_etapa,
            self.path_etapa,
            self.time_crea_etapa,
        )
        return info

    # se genera la tupla para modificar los registros existentes
    def get_tupla_for_update(self):
        info = (
            self.name_etapa,
            self.cat_id_etapa,
            self.path_etapa,
            self.time_crea_etapa,
            self.id_etapa,
        )  # se agrega el id_cat al final como parametro del where
        return info

    # Se realizan las updates a los registros
    def update_etapa(self):  # Retorna estatus
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ UPDATE "etapas"
            SET Titulo= '{}', Categoria_Id= {},  Ruta_Carpeta = '{}',
             Fecha_Creacion = {} WHERE Id_etapas= {} ;""".format(
            self.get_tupla_for_update()
        )
        try:
            cur.executescript(script)
            db.commit()
            return "Modificación exitoso"
        except sqlite3.Error as err:
            return "Error en la modificación del registro"
        finally:
            cur.close()

    # los getters para obtener los nombres y el id de los proyectos
    def get_titulos_etapa(
        self, id_cat
    ):  # Retorna los titulos de los proyectos para los spinners
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """ SELECT Titulo FROM "etapas" WHERE Categoria_Id = {} ORDER BY Id_categorias ;""".format(
            id_cat
        )
        try:
            cur.execute(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()

    def get_id_etapa_from_str(self, nom_cat, id_cat):
        db = sqlite3.connect(Sage.get_db())
        cur = db.cursor()
        script = """SELECT Id_categorias FROM "categorias" WHERE Titulo = '{}' AND Categoria_Id = {} ;""".format(
            nom_cat, id_cat
        )
        try:
            cur.executescript(script)
            return cur.fetchall()
        except sqlite3.Error as err:
            return "Error al realizar la consulta"
        finally:
            cur.close()
