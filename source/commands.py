import session
import query
import statics
import dataprint


def stats(inpt, info):
    sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.datastats(columns, results)
    input(statics.PAUSE)


def insert(inpt, info):
    chunk = []
    bit = []
    for i in inpt[1:]:
        if "-" in str(i):
            chunk.append(bit)
            bit = []
        else:
            bit.append(str(i))
    chunk.append(bit)

    inpt = [" ".join(i) for i in chunk]

    sql_query = "INSERT INTO " + info[1] + \
                "(" + ", ".join(statics.HOST_SET[info[1]]) + ") VALUES ('" + "', '".join(inpt) + "')"
    query.execute_sql(info[0], sql_query)
    info[0].commit()


def upload(inpt, info):
    with open(inpt[0], "r") as file:
        row = file.readline()
        while row:
            row = row.strip("\n").split(",")
            sql_query = "INSERT INTO " + info[1] + "(" + ", ".join(statics.HOST_SET[info[1]]) + ")" \
                                                   " VALUES('" + "', '".join(row) + "')"
            query.execute_sql(info[0], sql_query)
            info[0].commit()

            row = file.readline()


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
