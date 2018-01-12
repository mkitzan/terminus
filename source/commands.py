import session
import query
import statics
import dataprint

from math import ceil


def tsv(inpt, info):
    """Exports a search query to TSV."""
    sql_query = query.parse_sql(inpt, info[1], "search")
    
    columns, results = query.execute_sql(info[0], sql_query)
    fileout(columns, results, "\t", info[1])


def fileout(columns, results, delim, host):
    """Helper function to write a result set to a TSV file."""
    with open(host + ("-export.tsv" if delim == "\t" else "-export.csv"), "w") as outfile:
        outfile.write(delim.join(columns) + "\n")
        for row in results:
            outfile.write(delim.join([str(i) for i in row]) + "\n")


def sql(inpt, info):
    """Runs a raw SQL query."""
    # checks if query is accessing a blocked table
    for el in inpt:
        if el in statics.BLOCKED:
            return
    
    command = inpt.pop(0)
    sql_query = " ".join(inpt)
    columns, results = query.execute_sql(info[0], sql_query)
    
    if command == "search":
        dataprint.table(columns, results)
    elif command == "stats":
        dataprint.stats(columns, results)
    elif command == "tsv":
        fileout(columns, results, "\t", info[1])
        return
        
    input(statics.PAUSE)


def plot(inpt, info):
    """Preprocessing for dataprint's plot.
    Creates the augmented SQL query specifically for plot."""
    args = {"whr": [], "-X": [], "-Y": []}
    agg = ["count", "sum", "avg"]
    temp = []
    # WHERE exists, scale, operation type, aggregated axis
    spec_vars = [False, 1, "count", "-Y"]

    # creates lists of each flags arguments
    for el in reversed(inpt):
        if "-" in el:
            if el in args.keys():
                args[el] += reversed(temp)
            else:
                spec_vars[0] = True
                args["whr"] += [el]
                args["whr"] += reversed(temp)
            
            temp = []
        else:
            temp += [el]
    
    # finds the aggregate axis, sets variables for use in printing
    for el in (args["-X"] + ["-X"]) if len(args["-X"]) > 1 else (args["-Y"] + ["-Y"]):
        try:
            int(el)
            spec_vars[1] = int(el)
        except ValueError:
            if el in agg:
                spec_vars[2] = el
            elif el in args.keys():
                spec_vars[3] = el
    
    args[spec_vars[3]].remove(spec_vars[2])
    args[spec_vars[3]].remove(str(spec_vars[1]))
    op_flg = "-X" if spec_vars[3] == "-Y" else "-Y"
    
    sql_query = "SELECT " + ((args["-Y"][0] + ", " + args["-X"][0]) if spec_vars[3] == "-X" else (args["-X"][0] + ", " + args["-Y"][0])) + \
                " FROM " + info[1] + ((" WHERE " + query.parse_flags(args["whr"])) if spec_vars[0] else "") + " ORDER BY " + args[op_flg][0]

    columns, results = query.execute_sql(info[0], sql_query)
    
    dataprint.plot(columns, results, spec_vars[2], spec_vars[1], spec_vars[3][1].lower(), buffer_val=(0 if spec_vars[3][1] == "X" else 1))
    input(statics.PAUSE)


def cmd_stats(inpt, info):
    """Intermediary function for dataprint's stats function."""
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.stats(columns, results)
    input(statics.PAUSE)


def repackage(inpt, host):
    """Tosses out flags, and joins multi-word values together."""
    cols = [-1] * len(statics.HOST_SET[host])
    flag = 0

    for i in range(len(inpt)):
        curr = statics.ret_flag(inpt, i) if "-" == inpt[i][0] else ""

        if curr in statics.FLAGS.keys():
            cols[statics.HOST_SET[host].index(statics.FLAGS[statics.ret_flag(inpt, flag)])] = " ".join(inpt[flag+1:i])
            flag = i

    cols[statics.HOST_SET[host].index(statics.FLAGS[statics.ret_flag(inpt, flag)])] = " ".join(inpt[flag+1:])

    return cols
    
    
def insert(inpt, info):
    """Inserts a record into the current DB host table."""
    inpt = repackage(inpt, info[1])

    sql_query = "INSERT INTO " + info[1] + \
                "(" + ", ".join(statics.HOST_SET[info[1]]) + ") VALUES ('" + "', '".join(inpt) + "')"

    query.execute_sql(info[0], sql_query)
    info[0].commit()


def prepare_row(row):
    """Formats CSV so commas within quotes are not split upon."""
    row = row.split(",")
    st = None
    
    proc_row = []
    for i in range(len(row)):
        if st is None:
            if row[i][0] == "\"" and row[i][-1] != "\"":
                st = i
            else:
                proc_row += [row[i]]
        elif row[i][-1] == "\"":
            proc_row += [",".join(row[st:i+1])]
            st = None
            
    return proc_row


def upload(inpt, info):
    """Uploads a CSV or TSV into the current DB host table."""
    # loops through the file counting rows
    file_len = 0
    for line in open(inpt[0], "r"):
        file_len += 1
    
    # sets the row processing function depending on file format
    funct = (lambda r: "', '".join(prepare_row(r))) if inpt[0][-3:] == "csv" else (lambda r: r.replace("\t", "', '"))

    with open(inpt[0], "r") as file:
        row = file.readline().strip("\n")
        curr = 1
        
        while row:
            # processes progress ratios
            ratio = curr / file_len
            progress = ceil(ratio * statics.PROGRESS)
            ratio = ceil(ratio * 100)
            row = funct(row)

            # prints the progress bar
            session.clear_screen()
            print(info[2] + "@" + info[1] + ": " + "upload " + " ".join(inpt)) 
            print("\n    |" + ("#" * progress) + (" " * (statics.PROGRESS - progress)) + "|  " + str(ratio) + "%")
            print("\n    '" + row + "'")
            
            sql_query = "INSERT INTO " + info[1] + "(" + ", ".join(statics.HOST_SET[info[1]]) + ")" \
                                                   " VALUES('" + row + "')"

            query.execute_sql(info[0], sql_query)
            curr += 1
            row = file.readline().strip("\n")
    
        info[0].commit()


def remove(inpt, info):
    """Intermediary function to remove some set of records from the current DB host table."""
    sql_query = query.parse_sql(inpt, info[1], "remove")

    query.execute_sql(info[0], sql_query)
    info[0].commit()


def find_change(inpt):
    """Creates the change clause for the update function."""
    change = inpt.pop(0).capitalize() + "='"
    
    for i in range(len(inpt)):
        flg = statics.ret_flag(inpt, i) if "-" == inpt[i][0] else ""
        if flg in statics.FLAGS:
            change = change[:-1]
            break
        
        change += str(inpt[i]) + " "
            
    change += "'"
    inpt[:i] = []
    return change


def update(inpt, info):
    """Runs an update on the current DB host table."""
    criteria = "UPDATE " + info[1] + " SET " + find_change(inpt) + " WHERE "
    where = query.parse_flags(inpt)

    query.execute_sql(info[0], criteria + where)
    info[0].commit()


def sum(inpt, info):
    """Helper function for 'aggregate', passes SUM"""
    aggregate("SUM", inpt, info)


def count(inpt, info):
    """Helper function for 'aggregate', passes COUNT"""
    aggregate("COUNT", inpt, info)


def average(inpt, info):
    """Helper function for 'aggregate', passes AVG"""
    aggregate("AVG", inpt, info)  


def aggregate(agg, inpt, info):
    """Creates and runs a DB update."""
    sql_query = "SELECT " + agg + "(" + inpt[0] + ")" + " FROM " + info[1] + " WHERE " + query.parse_flags(inpt[1:])

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    input(statics.PAUSE)
    
    
def report(inpt, info):
    """Performs a search with the input, then passes the results to dataprint's export to create a simply report."""
    args = [el for el in inpt]
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.export(columns, results, info[1], "report " + " ".join(args), plot_res=True)


def search(inpt, info):
    """Runs a DB search then acts as an intermediary function for dataprint's table function."""
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    
    input(statics.PAUSE)
    
    
def find_op(inpt):
    """Cuts out args stating the operation to perform."""
    for i in range(len(inpt)):
        curr = inpt[i][1:3].upper() if len(inpt[i]) > 2 else inpt[i]
        
        if curr == "-C" and i+1 < len(inpt):
            op = inpt[i+1]
            inpt[i:i+2] = []
            return op
    
    
def distinct(inpt, info):
    """Executes a standard search query, then cuts out non-distinct records.
    After, executes dataprint functions: stats, report, or search on the results set."""
    op = find_op(inpt)
        
    sql_query = query.parse_sql(inpt[1:], info[1], "search")
    
    columns, results = query.execute_sql(info[0], sql_query)
    pivot = columns.index(inpt[0].capitalize())
    
    dist = set()
    dupl = []
    for i in range(len(results)):
        if results[i][pivot] in dist:
            dupl += [i]
        else:
            dist = dist.union({results[i][pivot]})
            
    dupl.reverse()
    for i in dupl:
        results.pop(i)
        
    if op == "stats":
        dataprint.stats(columns, results)
    elif op == "report":
        dataprint.export(columns, results, info[1], "distinct " + " ".join(inpt), plot_res=True)
        return
    elif op == "tsv":
        fileout(columns, results, "\t", info[1])
        return
    elif op == "search":
        dataprint.table(columns, results)

    input(statics.PAUSE)


def change(inpt, info):
    """Allows user to change the user, or host table."""
    length = len(inpt)

    for i in range(length):
        if (inpt[i] == "-h" or inpt[i] == "--host") and i+1 < length:
            if session.change_host(info[0], inpt[i+1]):
                info[1] = inpt[i+1]
            else:
                input(statics.HOST_ERROR.strip("\n"))
                return
                
            i += 1
        elif (inpt[i] == "-u" or inpt[i] == "--user") and i+2 < length:
            if session.verify(info[0], inpt[i+1], inpt[i+2]):
                info[2] = inpt[i+1]
            else:
                input(statics.LOGIN_ERROR.strip("\n"))
                return
                
            i += 2


def close_out(inpt, info):
    """Closes DB connection."""
    info[0].close()
    print(statics.CLOSE)


def cmd_help(inpt, info):
    """Prints the correctly formatted help page."""
    print(statics.help1(info[1]))

    for i in statics.HOST_SET[info[1]]:
        print(statics.FLAG_HELP[i])

    print(statics.HELP_STANDARD)

    for el in inpt:
        print(statics.help2(el))
        print(statics.HELP_TEXT[el] if el in query.FUNCTIONS.keys() else statics.CMD_ERROR)

    input(statics.PAUSE)
