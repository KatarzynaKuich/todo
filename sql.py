import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


if __name__ == "__main__":

    create_todos_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS todos (
      id integer PRIMARY KEY,
      title text NOT NULL,
      description text,
      done text
   );
   """
    db_file = "database.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_todos_sql)
        conn.close()


def add_todo(conn, todo):
    """
       Create a new todo into the projects table
       :param conn:
       :param todo:
       :return: todo id
       """

    sql = '''INSERT INTO todos(title, description, done)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, todo)
    conn.commit()
    return cur.lastrowid


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

        update(conn, "todos", 1)
        delete_all(conn, "todos")
        conn.close()
