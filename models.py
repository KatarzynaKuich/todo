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
                   CREATE TABLE IF NOT EXISTS books (
                       id integer PRIMARY KEY,
                       title text NOT NULL,
                       description text NOT NULL,
                       done boolean not null
                   );
                   """)


def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def update(conn, table, id, **kwargs):
    """
    update title, desctption, and done
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)

    def delete_all(conn, table):
        """
        Delete all rows from table
        :param conn: Connection to the SQLite database
        :param table: table name
        :return:
        """
        sql = f'DELETE FROM {table}'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Deleted")

    if __name__ == "__main__":
        todo = ("odrobic lekcje", "musze napisac projekt", "true")

        conn = create_connection("database.db")

        todo_id = add_todo(conn, todo)

        print(todo_id)
        conn.commit()
        select_all(conn,"todos")
        update(conn, "todos", 1)
        delete_all(conn, "todos")
        conn.close()
todos=TodosSQLite()