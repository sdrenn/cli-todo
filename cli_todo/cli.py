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

    def remove(self, ids):
        self.cur.execute('delete from todo where id in (?)', ids)


class Db:
    def __init__(self):
        self.con = self.get_db()
        self.cur = self.con.cursor()
        self.cur.execute("SELECT name FROM sqlite_schema WHERE type='table'")
        tables = list(self.cur.fetchall())
        if ('todo',) not in tables:
            self.cur.execute('create table todo (id integer primary key, text text, done bool)')

    def __enter__(self):
        return DbCur(self.cur)

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()

    def get_db(self):
        return sqlite3.connect('todo.db')


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
    with Db() as cur:
        cur.add(todo)


@cli.command()
def remove(indexes: list[int]):
    '''
    Remove TODO by index
    '''
    with Db() as cur:
        cur.remove(indexes)


@cli.command('list')
def get_list():
    '''
    List of TODOs
    '''
    with Db() as cur:
        for i, todo, done in cur.select():
            print(f'{i}, {todo}, {done}')
