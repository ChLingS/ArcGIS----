import sqlite3
from flask import g


DATABASE = '/usr/local/python3.8.6/workspace/DATADB/早稻.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_all_data(table_name:str) -> list:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rv = cur.fetchall()
    cur.close()
    return rv

def get_all_colums(table_name:str) -> list:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    column_names = [row[1] for row in columns]
    cur.close()
    return column_names

def get_all_citys() -> list:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    table_names = [row[0] for row in tables]
    cur.close()
    return table_names

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()  