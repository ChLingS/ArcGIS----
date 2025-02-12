import sqlite3
from flask import g


DATABASE = '/usr/local/python3.8.6/workspace/DATADB/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]  # 获取列名
    cur.close()

    # 如果 one=True 并且查询结果非空，返回第一个结果作为字典
    if one and rv:
        return dict(zip(colnames, rv[0]))
    else:
        # 如果 one=False 或者没有结果，返回所有结果（作为元组的列表）
        # 如果你想返回列表的字典，可以遍历 rv 并为每个元组创建一个字典
        # return [dict(zip(colnames, row)) for row in rv]
        return rv


def execute_db(query, args=()):
    db = get_db()
    cur = db.cursor()
    print(query)
    cur.execute(query, args)
    db.commit()  # 对于非查询操作，通常需要提交事务
    cur.close()

