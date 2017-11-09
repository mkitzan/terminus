import os
import hashlib
import sqlite3
import getpass
import time
import query
import statics


def new_user(inpt, connection):
    sql_query = "INSERT INTO credentials VALUES('" + hash_credentials(inpt[0], inpt[1]) + "')"
    query.execute_sql(connection, sql_query)
    connection.commit()


def create_record(inpt, info):
    sql_query = "INSERT INTO records VALUES('" + time.strftime("%d/%m/%Y %H:%M:%S") + "', '" + info[2] + "', '" + \
                inpt[0] + "', '" + info[1] + "', '" + " ".join(inpt[1:]) + "')"
    query.execute_sql(info[0], sql_query)
    info[0].commit()


def hash_credentials(text, key):
    hasher = hashlib.sha256()
    hasher.update(bytes(text+key, "utf-8"))
    
    return hasher.hexdigest()


def verify(db, username, password):
    hash_key = hash_credentials(username, password)

    curs = db.cursor()
    curs.execute("SELECT * FROM credentials WHERE Hash='" + hash_key + "'")

    if curs.fetchone() is None:
        curs.close()
        return False
    else:
        curs.close()
        return True


def change_user(db):
    valid = False

    while not valid:
        clear_screen()
        user = input("Username: ")
        password = getpass.getpass("Password: ")
        clear_screen()

        valid = verify(db, user, password)
        if not valid:
            print("Invalid login credentials")
            input()

    return user


def direct_host_change(db, host):
    if host == "sqlite_master" or host == "credentials":
        return False

    curs = db.cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE name='" + host + "'")
    
    if curs.fetchone() is not None:
        curs.close()
        return True
    else:
        curs.close()
        return False


def change_host(db):
    valid = False

    while not valid:
        clear_screen()
        host = input("Enter Host: ")

        valid = direct_host_change(db, host)
        if not valid:
            print("Invalid host table")
            input()

    return host


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
        
def resize():
    if os.system == "nt":
        print("todo")
    else:
        os.system("resize -s " + str(statics.HEIGHT) + " " + str(statics.WIDTH))


def title():
    if os.system == "posix":
        os.system("echo -e '\033]2;'" + statics.VERSION + "'\007'")
    else:
        os.system("title " + statics.VERSION)


def get_connection():
    return sqlite3.connect("library.db")
