import sqlite3 as sq


def sql_start():
    base = sq.connect('smart_connect.db')
    if base:
        print('База данных подключена.')

    # base.execute('''DROP TABLE IF EXISTS users''')
    # base.execute('''DROP TABLE IF EXISTS interests''')
    # base.execute('''DROP TABLE IF EXISTS users_interests''')

    base.execute(
        'CREATE TABLE IF NOT EXISTS interests('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' interest_name TEXT UNIQUE,'
        ' interest TEXT UNIQUE);'
    )
    
    base.execute(
        'CREATE TABLE IF NOT EXISTS users('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' user_tg_id TEXT,'
        ' user_name TEXT,'
        ' sex TEXT,'
        ' age INTEGER CHECK(age >= 16),'
        ' tg_link TEXT,'
        ' registration_date TEXT,'
        ' email TEXT,'
        ' education TEXT,'
        ' FOREIGN KEY (id) REFERENCES users_interests(user_id)'
        ');'
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


# Запросы

async def get_user(user_tg_id):
    base = sq.connect('smart_connect.db')
    cur = base.cursor()

    user = cur.execute('''
        SELECT * FROM users WHERE user_tg_id = ?
    ''', (user_tg_id,)).fetchone()

    base.close()

    return user


async def create_user(*args):
    base = sq.connect('smart_connect.db')
    cur = base.cursor()

    cur.execute('''
            INSERT INTO users (user_tg_id, user_name, tg_link, registration_date)
            VALUES (?, ?, ?, ?);
        ''', (*args,))

    base.commit()
    base.close()


async def update_user(user_tg_id, **kwargs):
    base =sq.connect('smart_connect.db')
    cur = base.cursor()

    cur.execute('''
        INSERT OR IGNORE INTO interests (interest_name) VALUES (?);
    ''', (kwargs['interest_category'],))

    if cur.lastrowid is not None:
        interest_id = cur.lastrowid
        print(f"Запись добавлена успешно. ID записи: {interest_id}")
    else:
        cur.execute('''
            SELECT id FROM interests WHERE interest_name = ?;
        ''', (kwargs['interest_category'],))
        interest_id = (cur.fetchone())[0]
        print("Запись уже существует.")

    cur.execute('''
        SELECT id FROM users WHERE user_tg_id = ?;
    ''', (user_tg_id,))
    user_id = (cur.fetchone())[0]

    cur.execute('''
        INSERT INTO users_interests (interest_id, user_id, experience_level) VALUES (?, ?, ?);
    ''', (interest_id, user_id, kwargs['experience']))

    cur.execute('''
        UPDATE users SET sex = ?, age = ?, education = ?, email = ? WHERE user_tg_id = ?;
    ''', (kwargs['sex'], kwargs['age'], kwargs['education'], kwargs.get('email', "None"), user_tg_id))

    base.commit()
    base.close()
