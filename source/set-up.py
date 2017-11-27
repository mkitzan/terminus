import session
import query
import getpass
import statics


def help():
    session.clear_screen()
    print(statics.SETUP_HELP)
    input(statics.PAUSE)


def close_out():
    session.clear_screen()
    exit()


def new_table():
    #table name
    #cols: label, type, spec
    print("todo")


def new_user():
    print(statics.SQLITE3)
    check = input(statics.HAS_SQLITE3)

    if check.lower() == "n":
        exit()

    user, password = get_user()
    create_user([user, password], session.get_connection())


def create_user(inpt, connection):
    sql_query = "INSERT INTO credentials VALUES('" + session.hash_credentials(inpt[0], inpt[1]) + "')"
    query.execute_sql(connection, sql_query)
    connection.commit()
    connection.close()


def get_user():
    match = False
    
    while not match:
        session.clear_screen()
        user = input(statics.NEW_USER)
        password = getpass.getpass(statics.NEW_PW)
        confirm = getpass.getpass(statics.CONFIRM_PW)
    
        match = True if password == confirm else False

    return user, password
    

def get_command():
    cont = True
    commands = {"user": new_user, "table": new_table, "help": help, "exit": close_out}

    while cont:
        session.clear_screen()
        print(statics.VERSION + statics.SETUP_OPTIONS)
        cmd = input(">>> ")
        print()
        cmd = "help" if cmd not in commands.keys() else cmd
        commands[cmd]()


def main():
    session.title()
    session.resize()
    session.clear_screen()
    
    print(statics.TITLE)
    print(statics.SETUP_MSG)
    input(statics.PAUSE)
    
    get_command()


if __name__ == "__main__":
    main()
