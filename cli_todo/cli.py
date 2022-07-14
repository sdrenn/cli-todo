import click
import sqlite3


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


@click.group()
def cli():
    pass


@cli.command()
@click.option('-t', '--text', prompt='Text', type=str, required=True)
def add(text):
    todo = Todo(text)
    with db as cur:
        cur.add(todo)


@cli.command()
@click.argument('index', type=int)
def remove(index):
    with db as cur:
        cur.remove(index)


@cli.command()
def list():
    with db as cur:
        for i, todo, done in cur.select():
            click.echo(f'{i}, {todo}, {done}')
