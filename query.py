import session
import commands
import statics


def execute_sql(db, sql_query):
    curs = db.cursor()
    
    curs.execute(sql_query)
    columns = None
    if curs.description is not None:
        columns = [i[0] for i in curs.description]
        
    results = curs.fetchall()

    curs.close()
    
    return columns, results


def sorting(args):
    sort = ""
    index = (args.index("-s") if "-s" in args else args.index("--sort") if "--sort" in args else -1)

    if index != -1:
        sort += " ORDER BY " + args.pop(index + 1)
        args.pop(index)

    return sort


def parse_flags(args):
    columns = {k: 0 for k in statics.ALL_COLUMNS}

    where = ""

    sort = sorting(args)

    for i in range(len(args)):
        arg = str(args[i])
        curr = arg[1:3] if len(arg) > 2 else arg

        if curr in statics.FLAGS.keys():
            where = where[:-1] + "' and " + statics.FLAGS[curr] + "='"
            columns[statics.FLAGS[curr]] = 1
            
        else:
            where += arg + " "

    return where[6:-1] + "'" + sort, columns
    
    
def order_columns(columns):
    return [i for i in statics.ALL_COLUMNS if i in columns]


def parse_sql(args, host, operation):
    where, columns = parse_flags(args)
        
    columns = [i for i in statics.HOST_SET[host] if columns[i] == 0]

    if operation == "remove":
        sql_query = "DELETE FROM " + host
    elif operation == "complete":
        sql_query = "UPDATE " + host + " SET Finished='true'"
    else:
        columns = order_columns(columns)
        sql_query = "SELECT " + ", ".join(columns) + " FROM " + host

    return sql_query + " WHERE " + where


def run_command(command, info):
    command = command.split(" ")
    functions = {"search": commands.search, "insert": commands.insert,
                 "remove": commands.remove, "complete": commands.complete,
                 "exit": commands.close_out, "aggregate": commands.aggregate,
                 "change": commands.change, "help": commands.cmd_help,
                 "upload": commands.upload}
    
    if command[0] not in functions.keys():
        print("Invalid function '" + command[0] + "': enter 'help' for more information.")
    else:
        print()
        try:
            session.create_record(command, info)
            functions[command[0]](command[1:], info)
        except:
            input("Error occurred while executing.\nTry: help " + (command[0] if command[0] != "help" else ""))

    if command[0] == "exit":
        return False
    else:
        return True


def landing(info):
    not_done = True

    while not_done:
        session.clear_screen()

        command = input(info[2] + "@" + info[1] + ": ")
        
        not_done = run_command(command, info)
