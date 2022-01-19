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
