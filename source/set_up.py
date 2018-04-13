import session
import query
import theme

from getpass import getpass


def help():
    """Prints set-up help text."""
    session.clear_screen()
    print(theme.SETUP_HELP)
    input(theme.PAUSE)


def close_out():
    """Safely exits set-up."""
    session.clear_screen()
    exit()


def new_table(connection=None):
    """Helper function for table, passes 'create'."""
    arg = True if connection is None else False
    connection = connection if connection is not None else session.get_connection()
    
    table("create", connection)
    
    if arg:
        connection.close()
    
    
def new_column(connection=None):
    """Helper function for table, passes 'alter'"""
    arg = True if connection is None else False
    connection = connection if connection is not None else session.get_connection()
    
    table("alter", connection)
    
    if arg:
        connection.close()

    
def table(operation, connection):
    """Gathers user input for altering or creating a table."""
    not_finished = True
    
    while not_finished:
        session.clear_screen()
        print(theme.TABLE)
        table = input(theme.NEW_TABLE)
        confirm = input(theme.CONFIRM_TABLE)
        
        not_finished = False if table == confirm else True
        
    not_finished = True
    
    while not_finished:
        session.clear_screen()
        print(theme.COLUMN_TEXT)
        
        column_space = []
        redo = False
        
        while not_finished: 
            col = []
            
            for text in theme.COLUMN_GET:
                col.append(input(text))
                if col[-1] == theme.END:
                    not_finished = False
                    break
                elif col[-1] == theme.REDO:
                    redo = True
                    break
            
            if redo:
                break    
            
            if operation == "alter":
                not_finished = False
                
            column_space.append(col)          
            print()
          
    session.clear_screen()
    
    if operation == "alter":
        alter_table(table, column_space, connection)    
        print(theme.adjust(table, operation) + theme.EXPLAIN2)
    else:
        create_table(table, column_space[:-1], connection)
        print(theme.adjust(table, operation) + theme.EXPLAIN1)
    
    input(theme.PAUSE)
   

def alter_table(table, columns, connection):
    """Creates SQL statement, and runs ALTER TABLE statement."""
    sql_statement = "ALTER TABLE " + table + " ADD COLUMN " + " ".join(columns[0]) + "\n"
    query.execute_sql(connection, sql_statement)
    connection.commit()

   
def create_table(table, columns, connection):
    """Creates SQL statement, and runs CREATE TABLE statement."""
    sql_statement = "CREATE TABLE IF NOT EXISTS " + table + " (\n" + ",\n".join([" ".join(col) for col in columns]) + "\n)"
    query.execute_sql(connection, sql_statement)
    connection.commit()


def new_user(connection=None):
    """Helper function which calls the user input function for the new user."""
    arg = True if connection is None else False
    connection = connection if connection is not None else session.get_connection()
    
    user, password = get_user()
    create_user([user, password], connection)
    
    if arg:
        connection.close()
        

def create_user(inpt, connection):
    """Creates the new user in the DB."""
    sql_statement = "INSERT INTO credentials VALUES('" + session.hash_credentials(inpt[0], inpt[1]) + "')"
    query.execute_sql(connection, sql_statement)
    connection.commit()


def get_user():
    """Gathers user info about the new user."""
    not_match = True
    
    while not_match:
        session.clear_screen()
        user = input(theme.NEW_USER)
        password = getpass(theme.NEW_PW)
        confirm = getpass(theme.CONFIRM_PW)
    
        match = False if password == confirm else True

    return user, password
    
    
def from_terminus(inpt, info):
    """Function the terminus core program uses to interface with set-up."""
    commands = {"user": new_user, "table": new_table, "column": new_column}
    
    for el in inpt:
        session.clear_screen()
        commands[el](connection=info[0])
    

def get_command():
    """Loop functions for users entering program directly from command line."""
    cont = True
    commands = {"user": new_user, "table": new_table, "column": new_column, "help": help, "exit": close_out}

    while cont:
        session.clear_screen()
        print(theme.VERSION + theme.SETUP_OPTIONS)
        cmd = input(theme.CHEVRON)
        print()
        cmd = "help" if cmd not in commands.keys() else cmd
        commands[cmd]()


def main():
    """Landing point for set-up when entered directly from command line."""
    session.title()
    session.clear_screen()
    
    print(theme.TITLE)
    print(theme.SETUP_MSG)
    input(theme.PAUSE)
    
    session.clear_screen()
    
    print(theme.SQLITE3)
    check = input(theme.HAS_SQLITE3)

    if check.lower() == "n":
        exit()
    
    get_command()


if __name__ == "__main__":
    main()
