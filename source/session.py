import query
import theme

from sqlite3 import connect
from os import name
from os import system 
from hashlib import sha256
from getpass import getpass
from time import strftime
from shutil import get_terminal_size


def change_pw(info, inpt):
    """Changes password in credentials table by deleting old hash and generating/inserting new hash"""
    password = ""
    valid = False

    while not valid:
        print()
        password = getpass("Enter old " + theme.GET_PW)

        valid = verify(info[0], info[2], password)
        
        if not valid:
            print(theme.PASS_ERROR[1:] + "\n")
            
    query.execute_sql(info[0], "DELETE FROM credentials WHERE Hash='" + hash_credentials(info[2], password) + "'")
    query.execute_sql(info[0], "INSERT INTO credentials VALUES('" + hash_credentials(info[2], inpt) + "')")


def change_username(info, inpt):
    """Changes username in credentials table by deleting old hash and generating/inserting new hash"""
    password = ""
    valid = False

    while not valid:
        print()
        password = getpass("Enter " + theme.GET_PW)

        valid = verify(info[0], info[2], password)
        
        if not valid:
            print(theme.PASS_ERROR[1:] + "\n")
            
    query.execute_sql(info[0], "DELETE FROM credentials WHERE Hash='" + hash_credentials(info[2], password) + "'")
    query.execute_sql(info[0], "INSERT INTO credentials VALUES('" + hash_credentials(inpt, password) + "')")


def create_record(inpt, info):
    """Creates and submits a record of a user inputted command."""
    sql_query = "INSERT INTO records VALUES('" + strftime(theme.DATE_TIME + " %H:%M:%S") + "', '" + info[2] + "', '" + \
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
    theme.SCRIPT_VARS["$trm.day"] = strftime("%d")
    theme.SCRIPT_VARS["$trm.year"] = strftime("%Y")
    theme.SCRIPT_VARS["$trm.date"] = strftime("%m/%d/%y")
    theme.DATE_TIME = strftime(theme.DATE_TIME)
    
    terminal_size()
    
    if name == "nt":
        theme.CLEAR = "cls"
    elif name == "posix":
        theme.TERMINAL_TITLE1 = "echo '\033]2;'"
        theme.TERMINAL_TITLE2 = "'\007'"


def clear_screen():
    """Clears the screen."""
    system(theme.CLEAR)


def title(extra=None):
    """Sets the terminal title."""
    system(theme.terminal_title(theme.VERSION + ("" if extra is None else (theme.TITLE_SEPARATOR + extra.capitalize()))))


def get_connection():
    """Creates a connection to the DB"""
    return connect(theme.DB)
    

def start_session():
    """Landing point, sets info variables used through out the program.
    Also print the title screen."""
    system_vars()
    title()
    clear_screen()
    
    # info[0] = sqlite DB connection
    # info[1] = current host table
    # info[2] = user name (for printing the command prompt)
    info = [None, None, None]
    info[0] = get_connection()
    
    print(theme.TITLE)
    theme.on_start(info[0])
    input(theme.PAUSE)
    clear_screen()
    
    # sets info variables used throughout active session
    info[1], info[2] = login(info[0])
    title(theme.DEFAULT_HOST)
    
    return info  
    

def main():
    """Calls function to init the session, then transfers control to the core loop."""
    info = start_session()
    query.landing(info)
    clear_screen()
    exit()
    
 
if __name__ == "__main__":
    main()
    
