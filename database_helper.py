import sqlite3


def initialize_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE packages (Name TEXT, Version TEXT, ID TEXT NOT NULL PRIMARY KEY, URL TEXT, Filename '
                 'TEXT)')
    print("Table created successfully")
    conn.close()


def post_package(name, version, p_id, url, filename):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO packages (Name,Version,ID,URL,Filename) \
        VALUES(?, ?, ?, ?, ?)", (name, version, p_id, url, filename))

        con.commit()


def get_package_by_id(id):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    res = cur.execute("select Name,Version from packages WHERE ID=" + str(id))

    for row in res:
        print(row)


if __name__ == '__main__':
    #initialize_db()
    post_package('test1', '1.0.2', '1', 'github.test', 'test1_content.txt')
    #get_package_by_id('1')
