import session
import commands
import statics


# function dictionary which is used to correctly call the user's command
FUNCTIONS = {"search": commands.search, "insert": commands.insert,
             "remove": commands.remove, "update": commands.update,
             "exit": commands.close_out, "sum": commands.sum,
             "count": commands.count, "avg": commands.average,
             "plot": commands.plot, "change": commands.change, 
             "help": commands.cmd_help, "upload": commands.upload, 
             "stats": commands.cmd_stats, "report": commands.report, 
             "distinct": commands.distinct, "sql": commands.sql,
             "tsv": commands.tsv}


def execute_sql(db, sql_query):
    """Runs the generated sql_query on the DB.
    Returns the result set, and column labels."""
    curs = db.cursor()
    curs.execute(sql_query)
    columns = None
    
    # cuts the out the empty values which result from the sqlite3 'description' attribute
    if curs.description is not None:
        columns = [i[0] for i in curs.description]
        
    results = curs.fetchall()
    curs.close()
    
    return columns, results


def sorting(args):
    """Creates the ORDER BY clause of flag input."""
    sort = ""
    index = (args.index("-s") if "-s" in args else args.index("--sort") if "--sort" in args else -1)

    if index != -1:
        sort += " ORDER BY "
        end = 0
        
        for i in range(index + 1, len(args)):
            if (args[i][1:3] if len(args[i]) > 2 else args[i]) not in statics.FLAGS.keys():
                sort += args[i] + ", "
                end = i
            else:
                break
                
        # deletes the sorting flag/arguments from the inpt list
        args[index:end+1] = []
        
    return sort[:-2]


def parse_flags(args):
    """Core flag to WHERE clause 'compiler'."""
    where = ""
    sort = sorting(args)

    for i in range(len(args)):
        arg = str(args[i]).replace("*", "%").replace("?", "_")
        curr = statics.ret_flag(args, i) if "-" == args[i][0] else ""
        # arg[1:3] if len(arg) > 2 else arg

        if curr in statics.FLAGS.keys():
            where = where[:-1] + "') AND (" + statics.FLAGS[curr] + " LIKE '"
        # processes logical operations in flag args
        elif arg in statics.LOGIC_OPS.keys():
            arg = statics.LOGIC_OPS[arg]
            where = where.split(" ")
            flag = "Title"
            
            for el in reversed(where[:-1]):
                el = el.strip("(")

                if el in statics.FLAG_HELP.keys():
                    flag = el
                    break
                    
            where = " ".join(where[:arg[0]]) + ((" (" + arg[1][1:]) if ("(" in where[arg[0]]) else arg[1]) + flag + " LIKE '" 
        else:
            where += arg + " "
    
    return where[7:-1] + "')" + sort


def parse_sql(args, host, operation):
    """Concatenates the bits of the SQL query together."""
    where = parse_flags(args)
    
    sql_query = statics.PARSE.setdefault(operation, lambda h: "SELECT " + ", ".join(statics.HOST_SET[h]) + " FROM " + h)(host)

    return sql_query + " WHERE " + where


def run_command(command, info):
    """Runs through the function dictionary, and calls the correct command with the user's input."""
    command = command.split(" ")
    
    if command[0] not in FUNCTIONS.keys():
        input(statics.funct_err(command[0]))
    else:
        print()
        try:
            session.create_record(command, info)
            FUNCTIONS[command[0]](command[1:], info)
        except Exception as e:
            # print error message
            input(str(e) + statics.EXCEPT + (command[0] if command[0] != "help" else ""))

    return False if command[0] == "exit" else True


def landing(info):
    """Loop which queries user for commands to run on the DB."""
    not_done = True

    while not_done:
        session.clear_screen()
        command = input(info[2] + "@" + info[1] + ": ")
        not_done = run_command(command, info)
