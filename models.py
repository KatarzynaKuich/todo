import json
import sqlite3


class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id]

    def create(self, data):
        data.pop('csrf_token')
        self.todos.append(data)

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.todos[id] = data
        self.save_all()


todos = Todos()


class TodosSQLite:
    def __init__(self):
        self.db_file = "database.db"
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
                   -- projects table
                   CREATE TABLE IF NOT EXISTS todos (
                       id integer PRIMARY KEY,
                       title text NOT NULL,
                       description text NOT NULL,
                       done boolean not null
                   );
                   """)

    def all(self):

        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM todos")
            rows = cur.fetchall()
            return rows

    def get(self, id):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM todos WHERE id=?", (id,))
            rows = cur.fetchall()
            return rows
    def create(self, data):

        sql = '''INSERT INTO todos(title, description, done)
                    VALUES(?,?,?)'''

        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            return cur.lastrowid

    def update(self, id, data):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            parameters = [f"{k} = ?" for k in data]
            parameters = ", ".join(parameters)
            values = tuple(v for v in data.values())
            values += (id,)
            sql = f''' UPDATE todos
                                SET {parameters}
                                WHERE id = ?'''
            try:
                cur.execute(sql, values)
                conn.commit()
                print("OK")
            except sqlite3.OperationalError as e:
                print(e)

    def delete_all(self):
        """
        Delete all rows from table
        :param conn: Connection to the SQLite database
        :param table: table name
        :return:
        """
        sql = f'DELETE FROM {self}'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Deleted")

todos = TodosSQLite()
