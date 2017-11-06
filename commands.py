import session
import query
import dataprint


PAUSE = "\nPress Enter to continue..."


def insert(inpt, info):
    where, columns = query.parse_flags(inpt)

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
    
    columns = [i for i in columns.keys() if columns[i] == 0]
    columns = query.order_columns(columns)
    
    sql_query = "INSERT INTO " + info[1] + "(" + ", ".join(columns) + ") VALUES('" + "', '".join(inpt) + "')"
    print(sql_query)
    query.execute_sql(info[0], sql_query)
    info[0].commit()


def upload(inpt, info):
    with open(inpt[0], "r") as file:
        row = file.readline()
        while row:
            row = row.strip("\n").split(",")
            sql_query = "INSERT INTO " + info[1] + "(Title, Author, Genre, Year, Pages, Type, Format, Finished)" \
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
    inpt[0].commit()


def aggregate(inpt, info):
    inpt[1][0].upper()

    if inpt[0] == "-avg" or inpt[0] == "--average":
        agg = "AVG(" + inpt[1] + ")"
    elif inpt[0] == "-sum" or inpt[0] == "--sum":
        agg = "SUM(" + inpt[1] + ")"
    else:
        agg = "COUNT(" + inpt[1] + ")"

    sql_query = "SELECT " + agg + " FROM " + info[1] + " WHERE " + query.parse_flags(inpt[2:])[0]

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    input(PAUSE)


def search(inpt, info):
    if "*" in inpt:
        sort = query.sorting(inpt)
        sql_query = "SELECT * FROM " + info[1] + sort
        print(sql_query)
    else:
        sql_query = query.parse_sql(inpt, info[1], "search")

    columns, results = query.execute_sql(info[0], sql_query)
    dataprint.table(columns, results)
    input(PAUSE)


def change(inpt, info):
    length = len(inpt)

    for i in range(length):
        if (inpt[i] == "-h" or inpt[i] == "--host") and i+1 < length:
            if session.direct_host_change(info[0], inpt[i+1]) is True:
                info[1] = inpt[i+1]
            else:
                print("Invalid host input")
                return
            i += 1
        elif (inpt[i] == "-u" or inpt[i] == "--user") and i+2 < length:
            if session.verify(info[0], inpt[i+1], inpt[i+2]) is True:
                info[2] = inpt[i+1]
            else:
                print("Invalid user input")
                return
            i += 2


def close_out(inpt, info):
    info[0].close()
    print("Database connection closed")


def cmd_help(inpt, info):
    print("""    Terminus supports 10 flags:
        -t or --title       flag specifies the title
        -a or --author      flag specifies the author
        -g or --genre       flag specifies the genre
        -y or --year        flag specifies the publishing year
        -p or --pages       flag specifies the page number
        -T or --type        flag specifies the type of book ie novel, short stories...
        -f or --format      flag specifies the book format ie paperback, hardcover...
        -F or --finished    flag specifies whether the book's been finished
        -c or --collection  flag specifies a short story's collection
        -q or --quote       flag specifies a book quote
        -s or --sort        flag specifies the sorting column\n
    Flag support by host:
        books:      -t, -a, -g, -y, -p, -T, -f, -F
        stories:    -t, -a, -g, -y, -p, -c
        quotes:     -t, -a, -y, -q\n
    Command list:
        search      perform SELECT SQL function
        insert      performs INSERT INTO SQL function
        remove      performs DELETE SQL function
        complete    performs UPDATE SQL function (only changes finished column to 'true')
        aggregate   performs AVG, SUM, and COUNT SQL functions
        change      allows host table and user change
        upload      allows for bulk insert from CSV file
        exit        safely exits program""")
    if len(inpt) > 0:
        if inpt[0] == "search":
            print("""
    Search supports special argument '*', selects all from host table (can still specify sorting)
    Example: search -a Harlan Ellison -T short stories""")
        elif inpt[0] == "insert":
            print("""
    Flag order is important for insert
    Example: insert -t Labryinths -a Jorge Luis Borges -g sf -y 1962 -p 251 -T short stories -f paperback -F false""")
        elif inpt[0] == "remove":
            print("""
    Example: remove -t Man Plus""")
        elif inpt[0] == "complete":
            print("""
    Example: complete -t A Scanner Darkly""")
        elif inpt[0] == "aggregate":
            print("""
    Aggregate has three additional flags:
        -cnt or --count     COUNT SQL function
        -sum or --sum       SUM SQL function
        -avg or --average   AVG SQL function\n
    Example: aggregate -cnt title -T short stories
    Count the title column where the type is 'short stories'""")
        elif inpt[0] == "change":
            print("""
    Change has two additional flags:
        -h or --host    specifies name of new host table
        -u or --user    takes two arguments following the flag: username password\n
    Example: change -h short stories -u test_user pw1234""")
        elif inpt[0] == "upload":
            print("""
    Upload takes no flag arguments, and file must be a csv with no column labels\n
    Expected column ordering by host table:
        books:      -t, -a, -g, -y, -p, -T, -f, -F
        stories:    -t, -a, -g, -y, -p, -c, -F
        quotes:     -t, -a, -y, -q\n
    Example: upload /path/to/file/if/not/in/curr/directory/test_upload.csv
    If an item in the upload has a column value with a comma, insert that item individually""")
        elif inpt[0] == "exit":
            print("""
    Exit takes no arguments used to safely leave the program""")

    input(PAUSE)
