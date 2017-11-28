import session
import query
import statics
import dataprint

from math import ceil


def cmd_stats(inpt, info):
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.stats(columns, results)
    input(statics.PAUSE)


def repackage(inpt):
    cols = []
    vals = ""
    for i in inpt[1:]:
        curr = i[1:3] if len(i) > 2 else i
        if curr in statics.FLAGS.keys():
            cols += [vals[:-1]]
            vals = ""
        else:
            vals += str(i) + " "
    cols += [vals[:-1]]
    
    return cols
    
    
def insert(inpt, info):
    inpt = repackage(inpt)

    sql_query = "INSERT INTO " + info[1] + \
                "(" + ", ".join(statics.HOST_SET[info[1]]) + ") VALUES ('" + "', '".join(inpt) + "')"
    query.execute_sql(info[0], sql_query)
    info[0].commit()


def upload(inpt, info):
    file_len = 0
    for line in open(inpt[0], "r"):
        file_len += 1

    with open(inpt[0], "r") as file:
        row = file.readline()
        curr = 1
        
        while row:
            ratio = curr / file_len
            progress = ceil(ratio * statics.PROGRESS)
            ratio = ceil(ratio * 100)
            row = row.strip("\n").replace(",", "', '")

            session.clear_screen()
            print(info[2] + "@" + info[1] + ": " + "upload " + inpt[0]) 
            print("\n    |" + ("#" * progress) + (" " * (statics.PROGRESS - progress)) + "|  " + str(ratio) + "%")
            print("\n    '" + row + "'")
            
            sql_query = "INSERT INTO " + info[1] + "(" + ", ".join(statics.HOST_SET[info[1]]) + ")" \
                                                   " VALUES('" + row + "')"
            query.execute_sql(info[0], sql_query)
    
            curr += 1
            row = file.readline()
    
    info[0].commit()


def remove(inpt, info):
    sql_query = query.parse_sql(inpt, info[1], "remove")

    query.execute_sql(info[0], sql_query)
    info[0].commit()


def complete(inpt, info):
    sql_query = query.parse_sql(inpt, info[1], "complete")

    query.execute_sql(info[0], sql_query)
    info[0].commit()


def sum(inpt, info):
    aggregate("SUM", inpt, info)


def count(inpt, info):
    aggregate("COUNT", inpt, info)


def average(inpt, info):
    aggregate("AVG", inpt, info)  


def aggregate(agg, inpt, info):
    sql_query = "SELECT " + agg + "(" + inpt[0] + ")" + " FROM " + info[1] + " WHERE " + query.parse_flags(inpt[1:])

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    input(statics.PAUSE)


def search(inpt, info):
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    input(statics.PAUSE)


def change(inpt, info):
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
    info[0].close()
    print(statics.CLOSE)


def cmd_help(inpt, info):
    print("    " + statics.VERSION + " '" + info[1] + "' supported flags: ")

    for i in statics.HOST_SET[info[1]]:
        print(statics.FLAG_HELP[i])

    print(statics.HELP_STANDARD)

    if len(inpt) > 0:
        print("\n    Command help '" + inpt[0] + "': ")
        print(statics.HELP_TEXT[inpt[0]] if inpt[0] in query.FUNCTIONS.keys() else statics.CMD_ERROR)

    input(statics.PAUSE)
