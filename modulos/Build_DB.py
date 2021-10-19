import sqlite3

def build(file):
    con = sqlite3.connect(file)

    try:
        # TABLA PROYECTOS
        con.execute("""
                CREATE TABLE "proyectos" (
                    "Id_proyecto"	INTEGER,
                    "Titulo"	TEXT,
                    "Descripcion"	LONGTEXT,
                    "Estatus"	INTEGER DEFAULT 1,
                    "Ruta_Carpeta"	longtext,
                    "Fecha_Creacion"	INTEGER,
                    PRIMARY KEY("Id_proyecto" AUTOINCREMENT)
                );
        """) 

        #TABLA CATEGORÍAS
        con.execute("""
                CREATE TABLE "categorias" (
                    "Id_categorias"	INTEGER UNIQUE,
                    "Titulo"	TEXT UNIQUE,
                    "Descripcion"	TEXT,
                    "Estatus"	INTEGER,
                    "Proyecto_Id"	INTEGER,
                    "Ruta_Carpeta"	TEXT,
                    "Fecha_Creacion"	INTEGER,
                    PRIMARY KEY("Id_categorias" AUTOINCREMENT),
                    FOREIGN KEY("Proyecto_Id") REFERENCES "proyectos"("Id_proyecto")
                );   
        """)  
        
        #TABLA ETAPAS
        con.execute("""
                    CREATE TABLE "etapas" (
                        "Id_etapa"	INTEGER UNIQUE,
                        "Titulo"	TEXT,
                        "Categoria_Id"	INTEGER,
                        "Ruta_Carpeta"	TEXT,
                        "Fecha_Creacion"	INTEGER,
                        FOREIGN KEY("Categoria_Id") REFERENCES "categorias"("Id_categorias"),
                        PRIMARY KEY("Id_etapa" AUTOINCREMENT)
                    );    
        """)  

        #TABLA TASKS
        con.execute("""
                    CREATE TABLE "tasks" (
                        "Id_Tasks"	INTEGER,
                        "Titulo"	TEXT DEFAULT 'Sin Titulo',
                        "Descripcion"	LONGTEXT,
                        "Estatus"	TEXT DEFAULT 'Registrada',
                        "Proyecto_Id"	INTEGER,
                        "Categoria_Id"	INTEGER,
                        "Etapa_Id"	INTEGER,
                        "Score"	INTEGER NOT NULL DEFAULT 0 CHECK("score" >= 0),
                        "Ruta_Carpeta"	TEXT,
                        "Fecha_Creacion"	INTEGER,
                        "Fecha_Inicial"	INTEGER,
                        "Fecha_Final"	INTEGER,
                        "Tipo_task"	TEXT,
                        FOREIGN KEY("Categoria_Id") REFERENCES "categorias"("Id_categorias"),
                        FOREIGN KEY("Etapa_Id") REFERENCES "etapas"("Id_etapa"),
                        FOREIGN KEY("Proyecto_Id") REFERENCES "proyectos"("Id_proyecto"),
                        PRIMARY KEY("Id_Tasks" AUTOINCREMENT)
                    );  
        """)  

        print("Se creó la tabla correctamente")
    except sqlite3.OperationalError:
        msg = "Error al crear las tablas"
        print(msg)

    con.close()     

