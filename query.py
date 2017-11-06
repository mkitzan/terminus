import session
import commands


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
    if "-s" in args:
        index = args.index("-s")
        sort += " ORDER BY " + args.pop(index + 1)
        args.remove("-s")
    elif "--sort" in args:
        index = args.index("--sort")
        sort += " ORDER BY " + args.pop(index + 1)
        args.remove("--sort")

    return sort


def parse_flags(args):
    columns = {"Author": 1, "Title": 1,
               "Genre": 1, "Format": 1,
               "Type": 1, "Year": 1,
               "Pages": 1, "Finished": 1,
               "Collection": 1, "Quote": 1}

    where = ""

    sort = sorting(args)

    length = len(args)

    for i in range(length):
        if str(args[i])[0] == "-":
            where = where[:-1] + "' and "
            if args[i] == "-a" or args[i] == "--author":
                where += "Author='"
                columns["Author"] = 0

            elif args[i] == "-t" or args[i] == "--title":
                where += "Title='"
                columns["Title"] = 0

            elif args[i] == "-g" or args[i] == "--genre":
                where += "Genre='"
                columns["Genre"] = 0

            elif args[i] == "-f" or args[i] == "--format":
                where += "Format='"
                columns["Format"] = 0

            elif args[i] == "-T" or args[i] == "--type":
                where += "Type='"
                columns["Type"] = 0

            elif args[i] == "-y" or args[i] == "--year":
                where += "Year='"
                columns["Year"] = 0

            elif args[i] == "-p" or args[i] == "--pages":
                where += "Pages='"
                columns["Pages"] = 0

            elif args[i] == "-F" or args[i] == "--finished":
                where += "Finished='"
                columns["Finished"] = 0

            elif args[i] == "-q" or args[i] == "--quote":
                where += "Quote='"
                columns["Quote"] = 0

            elif args[i] == "-c" or args[i] == "--collection":
                where += "Collection='"
                columns["Collection"] = 0

        else:
            where += str(args[i]) + " "

    return where[6:-1] + "'" + sort, columns
    
    
def order_columns(columns):
    all_cols = ["Title", "Author",
                "Genre", "Year",
                "Pages", "Type",
                "Format", "Finished",
                "Collection", "Quote"]
          
    ordered_cols = []
    for i in all_cols:
        if i in columns:
            ordered_cols.append(i)
    
    return ordered_cols


def parse_sql(args, host, operation):
    where, columns = parse_flags(args)

    if host == "books":
        columns = [i for i in columns.keys() - ["Quote", "Collection"] if columns[i] == 1]
    elif host == "stories":
        columns = [i for i in columns.keys() - ["Quote", "Format", "Type"] if columns[i] == 1]
    elif host == "quotes":
        columns = [i for i in columns.keys() - ["Collection", "Finished", "Format", "Type", "Pages", "Genre"] if columns[i] == 1]

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
