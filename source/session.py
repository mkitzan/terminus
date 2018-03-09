import query
import statics

from sqlite3 import connect
from os import name
from os import system 
from hashlib import sha256
from getpass import getpass
from time import strftime
from shutil import get_terminal_size


def create_record(inpt, info):
    """Creates and submits a record of a user inputted command."""
    sql_query = "INSERT INTO records VALUES('" + strftime("%m/%d/%Y %H:%M:%S") + "', '" + info[2] + "', '" + \
                inpt[0] + "', '" + info[1] + "', '" + " ".join(inpt[1:]) + "')"
    query.execute_sql(info[0], sql_query)
    info[0].commit()


def hash_credentials(text, key):
    """Performs the hash on user/password input."""
    hasher = sha256()
    hasher.update(bytes(text+key, "utf-8"))
    
    return hasher.hexdigest()


def verify(db, username, password):
    """Executes test on user/password input, and returns the truth value."""
    hash_key = hash_credentials(username, password)

    curs = db.cursor()
    curs.execute("SELECT * FROM credentials WHERE Hash='" + hash_key + "'")

    valid = (False if curs.fetchone() is None else True)
    curs.close()
    
    return valid


def login(db):
    """Loop which queries user for login credentials.
    Returns host, user information, which is used through out the session."""
    valid = False

    while not valid:
        clear_screen()     
        user = input(statics.GET_USER)
        password = getpass(statics.GET_PW)

        valid = verify(db, user, password)
        
        if not valid:
            input(statics.LOGIN_ERROR)
            continue
        
        if statics.DEFAULT_HOST is None or statics.DEFAULT_HOST in statics.BLOCKED:
            host = input(statics.GET_HOST)
            valid = change_host(db, host)
            
            if not valid:
                input(statics.HOST_ERROR)
        else:
            host = statics.DEFAULT_HOST

    return host, user


def change_host(db, host):
    """Aids changing host by first checking if suggested host exists in DB."""
    if host in statics.BLOCKED:
        return False

    curs = db.cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE name='" + host + "'")
    
    valid = (False if curs.fetchone() is None else True)
    curs.close()
    
    return valid
    
    
def terminal_size():
    """Sets variable related to the terminal size"""
    cols, rows = get_terminal_size()
    ratio = statics.BOUNDS / statics.WIDTH
    
    statics.WIDTH = cols
    statics.BOUNDS = statics.WIDTH - int(statics.WIDTH * ratio)
    
    if cols < statics.BOUNDS:
        # 14 = amount of constant space taken by progress bar
        statics.PROGRESS = abs(cols - 14)


def system_vars():
    """Sets variables often used throughout the active session."""
    terminal_size()
    
    if name == "nt":
        statics.CLEAR = "cls"
    elif name == "posix":
        statics.TERMINAL_TITLE = "echo -e '\033]2;'" + statics.VERSION + "'\007'"


def clear_screen():
    """Clears the screen."""
    system(statics.CLEAR)


def title(extra=""):
    """Sets the terminal title."""
    system(statics.TERMINAL_TITLE)


def get_connection():
    """Creates a connection to the DB"""
    return connect(statics.DB)
