import sqlite3
import shutil
import os.path
import defines
from datetime import timedelta,datetime

def category_is_empty(sql_cursor):
    sql_cursor.execute("SELECT COUNT(*) FROM category")
    sqL_result = sql_cursor.fetchone()
    return sqL_result[0] == 0

def create_goods_table(sql_cursor, name):
    sql_cursor.execute("""CREATE TABLE '""" + name + """'
                    (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    category_id INTEGER,
                    name text, 
                    description text, 
                    new_price INTEGER, 
                    old_price INTEGER)
                    """
                    )

def create_table(sql_cursor):
    sql_cursor.execute("""CREATE TABLE category
                  (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                  tag text, 
                  name text)
                  """)

    for day in range(defines.MAX_DAY_SAVE):
        create_goods_table(sql_cursor, 'goods_' + str(day))

    sql_cursor.execute("""CREATE TABLE table_date
              (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
              table_name text, 
              date text)
              """)

    date_table_data = []
    for day in range(defines.MAX_DAY_SAVE):
        date_table_data.append(["goods_" + str(day), "0"])

    sql_cursor.executemany("INSERT INTO table_date(table_name, date) VALUES (?,?)", 
        date_table_data)

    sql_cursor.execute("""CREATE TABLE added_goods
                    (category_id INTEGER,
                    name text, 
                    description text, 
                    new_price INTEGER, 
                    old_price INTEGER)
                    """)    

def backup_db():
    if not os.path.exists(defines.DB_FILE_NAME):
        return
    try:
        shutil.copy2(defines.DB_FILE_NAME, 'Backup'+defines.DB_FILE_NAME)
    except:
        print("Error backup databasee");       

def open():
    backup_db()
    sql_conn = sqlite3.connect(defines.DB_FILE_NAME)
    sql_cursor = sql_conn.cursor()
    try:
        create_table(sql_cursor)
        update(sql_cursor)
    except:
        #tables alredy exsist
        pass
    return sql_conn, sql_cursor

def update(sql_conn):
    sql_conn.commit()

def close(sql_conn, sql_cursor):
    update(sql_conn)
    sql_cursor.close()

def set_goods(sql_cursor, data, category_tag):
    sql_cursor.execute("SELECT id FROM category WHERE category.tag='"+category_tag+"'")
    category_id = sql_cursor.fetchone()
    sql_data = [(category_id[0], data[0], data[1], data[2])]
    sql_cursor.executemany("""
        INSERT INTO goods_0(category_id, name, description, new_price) 
        VALUES (?,?,?,?)""", sql_data)

def set_category(sql_cursor, data):
    sql_data = [data]
    sql_cursor.executemany("""INSERT INTO category(tag, name) 
        VALUES (?,?)""", sql_data)

def get_categories(sql_cursor):
    data = []
    sql_cursor.execute('SELECT tag, name  FROM category')
    for item in sql_cursor.fetchall():
        data.append([item[0], item[1]])

    return data

def clear_category(sql_cursor):
    sql_cursor.execute('DELETE FROM category')

def clear_goods(sql_cursor):
    sql_cursor.execute('DELETE FROM goods_0') 

def save_goods_table(sql_cursor):
    max_delta = defines.MAX_DAY_SAVE - 1
    for day in range(max_delta - 1, -1, -1):
        sql_cursor.execute('DELETE FROM goods_' + str(day + 1))
        sql_cursor.execute("INSERT INTO 'goods_" + str(day + 1) + "' SELECT * FROM 'goods_" + str(day) + "'") 
    
def calc_added_goods(sql_cursor):
    sql_cursor.execute('DELETE FROM added_goods') 
    #fill added_goods without category_id because category_id is chanded
    sql_cursor.execute("""INSERT INTO added_goods(name, description, new_price, old_price)
        SELECT name, description, new_price, old_price 
        FROM goods_0 
        EXCEPT 
        SELECT name, description, new_price, old_price 
        FROM goods_1""") 
    #update category_id
    sql_cursor.execute('UPDATE added_goods SET category_id=(SELECT category_id FROM goods_0 WHERE goods_0.name=added_goods.name)') 

def get_goods(sql_cursor, table_name):
    data = []

    sql_cursor.execute("SELECT category.id, category.name, category.tag FROM category, " +\
        table_name +\
        " WHERE category.id="+\
        table_name +\
        ".category_id GROUP BY category.name")

    for category in sql_cursor.fetchall():
        category_id = category[0]
        name = category[1]
        tag = category[2]

        sql_cursor.execute("SELECT name, description, new_price FROM "+\
            table_name+\
            " WHERE category_id = '" +\
            str(category_id) + "'" +\
            ' ORDER BY new_price') 

        goods = sql_cursor.fetchall()
        category_url = defines.url_from_tag(tag)

        #set [name, [[name, desc, new_price], ...] ]
        data.append([name, category_url, goods])

    return data

def get_added_goods(sql_cursor):
    return get_goods(sql_cursor, "added_goods")

def get_all_goods(sql_cursor):
    return get_goods(sql_cursor, "goods_0")    

def get_goods_time(sql_cursor):
    sql_cursor.execute("SELECT date FROM table_date WHERE table_name='goods_0'")
    time = sql_cursor.fetchone()[0]
    ttime = time.split(' ')
    return ttime[0]

def set_goods_time(sql_cursor):
    date = datetime.today()
    datetext = str(date)
    sql_data = [(datetext,)]
    sql_cursor.executemany("UPDATE table_date SET date=? WHERE table_name='goods_0'", sql_data)

def check_goods_time(sql_cursor):
    return True
    date = datetime.today()
    sql_cursor.execute("SELECT date FROM table_date WHERE table_name='goods_0'")
    dbtime = datetime.strptime(sql_cursor.fetchone()[0])
    delta = dbtime - date
    ret = delta >= datetime.time(hour=24)
    return ret