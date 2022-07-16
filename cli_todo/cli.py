import sqlite3
from typer import Typer, Option

cli = Typer()


class DbCur:
    def __init__(self, cur):
        self.cur = cur

    def add(self, todo):
        self.cur.execute("insert into todo values (NULL, ?, ?)", (todo.text, todo.done))

    def select(self):
        self.cur.execute("select * from todo")
        return self.cur.fetchall()

    def remove(self, i):
        self.cur.execute(f"delete from todo where id={i}")


class Db:
    def __init__(self):
        self.con = sqlite3.connect('todo.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT name FROM sqlite_schema WHERE type='table'")
        tables = list(self.cur.fetchall())
        if ('todo',) not in tables:
            print(tables)
            self.cur.execute('create table todo (id integer primary key, text text, done bool)')

    def __enter__(self):
        return DbCur(self.cur)

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()


db = Db()


class Todo:
    def __init__(self, text):
        self.text = text
        self.done = False

    def done(self):
        self.done = True


@cli.command()
def add(text: str = Option(..., prompt=True)):
    '''
    Add TODO
    '''
    todo = Todo(text)
    with db as cur:
        cur.add(todo)


@cli.command()
def remove(index: int):
    '''
    Remove TODO by index
    '''
    with db as cur:
        cur.remove(index)


@cli.command()
def list():
    '''
    List of TODOs
    '''
    with db as cur:
        for i, todo, done in cur.select():
            print(f'{i}, {todo}, {done}')
