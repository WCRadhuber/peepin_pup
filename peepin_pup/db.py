import psycopg2
import psycopg2.extras

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(current_app.config['DATABASE'])
        return g.db
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=()):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(query, args)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()
