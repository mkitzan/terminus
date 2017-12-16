import session
import commands
import statics


FUNCTIONS = {"search": commands.search, "insert": commands.insert,
             "remove": commands.remove, "update": commands.update,
             "exit": commands.close_out, "sum": commands.sum,
             "count": commands.count, "average": commands.average,
             "plot": commands.plot, "change": commands.change, 
             "help": commands.cmd_help, "upload": commands.upload, 
             "stats": commands.cmd_stats, "export": commands.export, 
             "distinct": commands.distinct}


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
        sort += " ORDER BY "
        end = 0
        
        for i in range(index + 1, len(args)):
            if (args[i][1:3] if len(args[i]) > 2 else args[i]) not in statics.FLAGS.keys():
                sort += args[i] + ", "
                end = i
            else:
                break
                
        args[index:end+1] = []
        
    return sort[:-2]


def parse_flags(args):
    where = ""
    sort = sorting(args)

    for i in range(len(args)):
        arg = str(args[i]).replace("*", "%").replace("?", "_")
        curr = arg[1:3] if len(arg) > 2 else arg

        if curr in statics.FLAGS.keys():
            where = where[:-1] + "' and " + statics.FLAGS[curr] + " LIKE '"
        else:
            where += arg + " "

    return where[6:-1] + "'" + sort


def parse_sql(args, host, operation):
    where = parse_flags(args)
    
    sql_query = statics.PARSE.setdefault(operation, lambda h: "SELECT " + ", ".join(statics.HOST_SET[h]) + " FROM " + h)(host)

    return sql_query + " WHERE " + where


def run_command(command, info):
    command = command.split(" ")
    
    if command[0] not in FUNCTIONS.keys():
        input(statics.funct_err(command[0]))
    else:
        print()
        try:
            session.create_record(command, info)
            FUNCTIONS[command[0]](command[1:], info)
        except Exception as e:
            input(str(e) + statics.EXCEPT + (command[0] if command[0] != "help" else ""))

    return False if command[0] == "exit" else True


def landing(info):
    not_done = True

    while not_done:
        session.clear_screen()
        command = input(info[2] + "@" + info[1] + ": ")
        not_done = run_command(command, info)
