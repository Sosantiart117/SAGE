import os 
import modulos.Build_DB as db

class Sage():

    db_file = os.path.join(os.getcwd() , "App_Data.db")

    @classmethod
    def get_db(cls):
        return cls.db_file

    @classmethod
    def init(cls):
        """ Metodo que inicia el ambiente para el programa """ 

        # Checa si hay base de datos
        if not os.path.isfile(cls.db_file): 
            db.build(cls.db_file)
