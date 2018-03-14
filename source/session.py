import query
import theme

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
        user = input(theme.GET_USER)
        password = getpass(theme.GET_PW)

        valid = verify(db, user, password)
        
        if not valid:
            input(theme.LOGIN_ERROR)
            continue
        
        if theme.DEFAULT_HOST is None or theme.DEFAULT_HOST in theme.BLOCKED:
            host = input(theme.GET_HOST)
            valid = change_host(db, host)
            
            if not valid:
                input(theme.HOST_ERROR)
        else:
            host = theme.DEFAULT_HOST

    return host, user


def change_host(db, host):
    """Aids changing host by first checking if suggested host exists in DB."""
    if host in theme.BLOCKED:
        return False

    curs = db.cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE name='" + host + "'")
    
    valid = (False if curs.fetchone() is None else True)
    curs.close()
    
    return valid
    
    
def terminal_size():
    """Sets variable related to the terminal size"""
    cols, rows = get_terminal_size()
    ratio = theme.BOUNDS / theme.WIDTH
    
    theme.WIDTH = cols
    theme.BOUNDS = theme.WIDTH - int(theme.WIDTH * ratio)
    
    if cols < theme.BOUNDS:
        # 14 = amount of constant space taken by progress bar
        theme.PROGRESS = abs(cols - 14)


def system_vars():
    """Sets variables often used throughout the active session."""
    theme.SCRIPT_VARS["$trm.weekday"] = strftime("%A")
    theme.SCRIPT_VARS["$trm.month"] = strftime("%B")
    theme.SCRIPT_VARS["$trm.day"] = strftime("%-d")
    theme.SCRIPT_VARS["$trm.year"] = strftime("%Y")
    theme.SCRIPT_VARS["$trm.date"] = strftime("%m/%d/%y")
    
    terminal_size()
    
    if name == "nt":
        theme.CLEAR = "cls"
    elif name == "posix":
        theme.TERMINAL_TITLE = "echo -e '\033]2;'" + theme.VERSION + "'\007'"


def clear_screen():
    """Clears the screen."""
    system(theme.CLEAR)


def title(extra=""):
    """Sets the terminal title."""
    system(theme.TERMINAL_TITLE)


def get_connection():
    """Creates a connection to the DB"""
    return connect(theme.DB)
