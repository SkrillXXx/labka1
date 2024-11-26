import sqlalchemy as sqla
CONNECTION_STRING = "mysql+pymysql://root@localhost/ww"

class Database():
    def __init__(self):
        self.engine = sqla.create_engine(CONNECTION_STRING)
        self.connection = self.engine.connect()

    def translate_to_dict(self, result_raw):
        result = []
        for r in result_raw:
            result.append(r._asdict())
        return result

    def get_news(self):
        query = sqla.text("SELECT * FROM pp")
        result_raw = self.connection.execute(query).all()
        return self.translate_to_dict(result_raw)

    def del_new(self, id):
        query = sqla.text("DELETE FROM pp WHERE id = :id")
        query = query.bindparams(sqla.bindparam("id", id))
        self.connection.execute(query)
        result = self.connection.commit()
        return result

    def add_new(self, name):
        query = sqla.text("INSERT INTO pp (name) VALUES (:name)")
        query = query.bindparams(sqla.bindparam("name", name))
        self.connection.execute(query)
        self.connection.commit()    

    def edit_new(self, name, id):
        query = sqla.text("UPDATE pp SET name = :name WHERE id = :id")
        query = query.bindparams(sqla.bindparam("name", name))
        query = query.bindparams(sqla.bindparam("id", id))
        self.connection.execute(query)
        self.connection.commit()

            
if __name__ == "__main__":
    db = Database()
    
    print(db.get_news(4))      