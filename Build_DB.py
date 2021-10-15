import sqlite3

con = sqlite3.connect("App_Data.db")

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
            
    """)  

    #TABLA TASKS
    con.execute("""
            
    """)  

    print("Se creó la tabla correctamente")
except sqlite3.OperationalError:
    msg = "Error al crear las tablas"
    print(msg)

con.close()     








# CREATE TABLE "etapas" (
# 	"Id_etapa"	INTEGER UNIQUE,
# 	"Titulo"	TEXT,
# 	"Categoria_Id"	INTEGER,
# 	"Ruta_Carpeta"	TEXT,
# 	"Fecha_Creacion"	INTEGER,
# 	FOREIGN KEY("Categoria_Id") REFERENCES "categorias"("Id_categorias"),
# 	PRIMARY KEY("Id_etapa" AUTOINCREMENT)
# );


# CREATE TABLE "tasks" (
# 	"Id_Tasks"	INTEGER,
# 	"Titulo"	TEXT DEFAULT 'Sin Titulo',
# 	"Descripcion"	LONGTEXT,
# 	"Estatus"	TEXT DEFAULT 'Registrada',
# 	"Proyecto_Id"	INTEGER,
# 	"Categoria_Id"	INTEGER,
# 	"Etapa_Id"	INTEGER,
# 	"Ruta_Carpeta"	TEXT,
# 	"Fecha_Creación"	INTEGER,
# 	"Fecha_Inicial"	INTEGER,
# 	"Fecha_Final"	INTEGER,
# 	PRIMARY KEY("Id_Tasks" AUTOINCREMENT),
# 	FOREIGN KEY("Categoria_Id") REFERENCES "categorias"("Id_categorias"),
# 	FOREIGN KEY("Proyecto_Id") REFERENCES "proyectos"("Id_proyecto"),
# 	FOREIGN KEY("Etapa_Id") REFERENCES "etapas"("Id_etapa")
# );