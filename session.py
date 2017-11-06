import os
import hashlib
import sqlite3
import getpass


VERSION = "Terminus vDEV"


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


def title():
    os.system("title " + VERSION)


def get_connection():
    return sqlite3.connect("library.db")
