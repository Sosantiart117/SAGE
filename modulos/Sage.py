class Sage():
    db_dir = "dbase.db"

    @classmethod
    def get_db(cls):
        return cls.db_dir