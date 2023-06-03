import sqlite3 as sq


def sql_start():
    base = sq.connect('smart_connect.db')
    if base:
        print('База данных подключена.')
    base.execute(
        'CREATE TABLE IF NOT EXISTS interests('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' interest_name TEXT,'
        ' interest TEXT);'
    )
    base.execute(
        'CREATE TABLE IF NOT EXISTS users('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' user_tg_id TEXT,'
        ' user_name TEXT,'
        ' sex TEXT,'
        ' age INTEGER CHECK(age >= 16),'
        ' tg_link TEXT,'
        ' registration_date TEXT);'
    )
    base.execute(
        'CREATE TABLE IF NOT EXISTS users_interests ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' interest_id INTEGER,'
        ' user_id INTEGER,'
        ' experience_level INTEGER,'
        ' FOREIGN KEY (interest_id) REFERENCES interests(id),'
        ' FOREIGN KEY (user_id) REFERENCES users(id));'
    )

    base.commit()
    base.close()
