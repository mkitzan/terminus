VERSION = "Terminus v2.7"

# font BIG, two spaces between name and ver: http://patorjk.com/software/taag/#p=display&f=Big&t=Terminus%20%20v2.8
TITLE = """
      _______                  _                         ___   ______ 
     |__   __|                (_)                       |__ \ |____  |
        | | ___ _ __ _ __ ___  _ _ __  _   _ ___   __   __ ) |    / / 
        | |/ _ \ '__| '_ ` _ \| | '_ \| | | / __|  \ \ / // /    / /  
        | |  __/ |  | | | | | | | | | | |_| \__ \   \ V // /_ _ / /   
        |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|___/    \_/|____(_)_/  
     Terminal Library Database
    """

# name of database to connect to
DB = "database/library.db"
DEFAULT_HOST = "books"

# terminal width
WIDTH = 130
# length of a line for quote at title screen
BOUNDS = 90
# length of progress bar in upload command
PROGRESS = 35

# error and pause text
PAUSE = "\nPress enter to continue..."
HOST_ERROR = "\nInvalid host input"
LOGIN_ERROR = "\nInvalid login credentials"
CMD_ERROR = "\n        Invalid command"
SCRIPT_ERROR = "\nScript must be a '.trm' file"
EXCEPT = "\nTry: help "

# logic ops available in queries val0 = back-index to cut list by, val1 = SQL argument
LOGIC_OPS = {"v": [-1, "' OR "], "^": [-1, "' AND "], "!": [-3, " NOT "]}

# names of tables not allowed to be accessed
BLOCKED = ["sqlite_master", "credentials"]

# special case operator when parsing arg flags to sql
PARSE = {"remove": lambda h: "DELETE FROM " + h}

# flag and column pairs for all columns throughout the DB
FLAGS = {"-a": "Author", "-t": "Title", "-g": "Genre", "-T": "Type",
         "-y": "Year", "-p": "Pages", "-f": "Format", "-F": "Finished", 
         "-c": "Collection", "-q": "Quote", "-d": "Day", "-o": "Operation",
         "-h": "Host", "-u": "User", "-A": "Arguments", "-P": "Priority",
         "-m": "Month", "-D": "Date", "-w": "Weekday"}
        
# all flags with capital short flags
CAPS = {"--type": "-T", "--finished": "-F", "--arguments": "-A", "--priority": "-P", "--date": "-D"}

# list of columns for each table (in order)
HOST_SET = {"books": ["Title", "Author", "Genre", "Year", "Pages", "Type", "Format", "Finished"],
            "stories": ["Title", "Author", "Genre", "Year", "Pages", "Collection", "Finished"],
            "quotes": ["Title", "Author", "Year", "Quote"],
            "wishlist": ["Title", "Author", "Genre", "Year", "Pages", "Type", "Priority"],
            "records": ["Date", "User", "Operation", "Host", "Arguments"],
            "tracker": ["Weekday", "Month", "Day", "Year", "Date", "Title", "Pages"]}

# help text for each flag/column
FLAG_HELP = {"Title": "        -t or --title       flag specifies the title",
             "Author": "        -a or --author      flag specifies the author",
             "Genre": "        -g or --genre       flag specifies the genre",
             "Year": "        -y or --year        flag specifies the year",
             "Pages": "        -p or --pages       flag specifies the page number",
             "Type": "        -T or --type        flag specifies the type of book ie novel, short stories...",
             "Format": "        -f or --format      flag specifies the book format ie paperback, hardcover...",
             "Finished": "        -F or --finished    flag specifies whether the book's been finished",
             "Collection": "        -c or --collection  flag specifies a short story's collection",
             "Month": "        -m or --month       flag specifies the month (abbreviated)",
             "Day": "        -d or --day         flag specifies the day numerial",
             "Weekday": "        -w or --weekday     flag specifies the weekday name (abbreviated)",
             "Quote": "        -q or --quote       flag specifies a book quote",
             "Date": "        -D or --date        flag specifies the date in mon/day/year",
             "User": "        -u or --user        flag specifies the user",
             "Operation": "        -o or --operation   flag specifies the operation used",
             "Host": "        -h or --host        flag specifies the host",
             "Arguments": "        -A or --arguments   flag specifies the command arguments",
             "Priority": "        -P or --priority    flag specifies the book's acquisition priority"}

# help text for each command function
HELP_TEXT = {"search": """        The go to command for querying the host table's records. 
        All the arguments following the command word specify the WHERE clause to query by.

        Example: search -a Harlan Ellison -T short stories""", 
             "insert": """        Inserts a records into the current host table. Flag order is not important for insert; however, all flags must be present.
             
        Example: insert -t Labryinths -a Jorge Luis Borges -g science fiction -y 1962 -p 251 -T stories -f paperback -F false""", 
             "remove": """        Used to delete records from the host table. The following arguments specify the WHERE clause to remove records by.
             
        Example: remove -t Man Plus""",
             "update": """        Update the first argument states the column where the update will take place, the next set states the change to be made.
        The following arguments state the WHERE clause to update records by.
        
        Example: update finished true -t A Scanner Darkly""", 
             "sum": """        Sums the values in the specified column. The following arguments specify the query's WHERE clause.
             
        Example: sum pages -T short stories""", 
             "count": """        Counts the values in the specified column. The following arguments specify the query's WHERE clause.
             
        Example: count title -F true""",
             "avg": """        Finds the average of values in the specified column. The following arguments specify the query's WHERE clause.
             
        Example: avg year -g science fiction""", 
             "change": """        Allows user to change the current host table, or user.
        Change has two additional flags:
            -h or --host    specifies name of new host table
            -u or --user    takes two arguments following the flag: username password
            
        Example: change -h short stories -u test_user pw1234""", 
             "plot": """        Plot prints a simple graph of an aggregated query
        Each axis flag needs a DB column specified, and one of those two states the aggregate type and the scale to plot by
        All non-axis arguments are interpreted in the standard 'search' format
        
        Example: plot -X author -Y count title 1 -g science fiction -F true""",
             "upload": """        Upload takes no flag arguments, the file format must be a CSV or TSV with no column label row.
        If an record in the upload file has a column value with a comma, insert that item individually.
        
        Expected column ordering by host table:
            books:      -t, -a, -g, -y, -p, -T, -f, -F
            stories:    -t, -a, -g, -y, -p, -c, -F
            tracker:    -w, -m, -d, -y, -D, -t, -p
            quotes:     -t, -a, -y, -q
            records:    -D, -u, -o, -h, -A
            wishlist:   -t, -a, -g, -y, -p, -T, -P
            
        Example: upload /path/directory/test_upload.csv""", 
             "stats": """        Creates a table of statistic values for a search query. All arguments are processed as a 'search' command.

        Example: stats -g science fiction -y 19??""",
             "report": """        Creates a simple report from the output of both a 'search', 'stats', and 'plot' call. 
        All arguments are processed as a 'search' command.
        
        Example: report -T stories -g science fiction -s author""",
             "distinct": """        Distinct allows for searching records with the distinct values in the specified column.
        Distinct value column is stated directly next to the 'distinct' command word.
        Unique flag '-C' or '--command' states how to run the arguments. Commands: 'search', 'stats', 'tsv', and 'report'
        
        Example: distinct title -F true -s author -C search""",
             "sql": """        The SQL command allows user to enter a raw SQL query. Useful for JOIN queries.
        The user must declare, immediately after the 'sql' keyword, either 'search', 'tsv', 'stats', or 'none' (if there's no output).
        
             
        Example: sql search SELECT Author, Year FROM books WHERE Year LIKE 19%%""",
             "export": """        Exports a TSV file of a search query. Useful when using Terminus data for other programs.
             
        Example: export -F false""",
             "system": """        Allows user ability to add new users, tables, or columns from inside the program.
        System has acceptable arguments corresponding to the new DB object to create: user, table, column.
        Multiple arguments can be present: they will be evaluated in order.
        
        Example: system user table""",
             "script": """        Declare the filename of the Terminus script (.trm) to be run with the '-S' flag. 
        Script variables must be declared with the '-v' flag. The var name and value must be stated with an '=' and no spaces. 
        Where ever a variable name appears as a distinct token in the script with a '$' preceding it, it will be replaced by the value at run time.
        Each line in the script will be interpreted as a Terminus command: blank lines will be disregarded.
        Users can access date related variables directly within a script: '$trm.weekday', '$trm.month', '$trm.day', '$trm.year', and '$trm.date'
        
        Example: script -S progress.trm -v title=Sturgeon is Alive and Well... pages=53
        Any appearances of '$title' would be replaced by 'Sturgeon is Alive and Well...', and '$pages' by '53'""",
             "exit": """        Exit takes no arguments. Used to safely leave the program.""",
             "help": """        Prints the general help page, and specific help pages for all the following arguments.
             
        Example: help plot stats upload"""}

# default help text
HELP_STANDARD = """
    Command list:
        search      performs the SELECT SQL function
        distinct    performs the SELECT DISTINCT SQL function
        insert      performs the INSERT INTO SQL function
        remove      performs the DELETE SQL function
        sum         performs the SUM SQL function
        count       performs the COUNT SQL function
        avg         performs the AVG SQL function
        update      performs the UPDATE SQL function
        plot        prints a simple graph of an aggregated query
        stats       outputs a statistics table on a 'search' command
        report      creates a simple report from query output
        change      allows host table and user change
        upload      allows for bulk 'insert' from CSV or TSV file
        sql         allows user to enter a raw SQL query
        export      allows user to export data as a TSV
        system      allows user to create new DB objects
        script      allows user to run a .trm script
        help        prints a general help page, and command specific help pages
        exit        safely exits program
        
    Terminus supports both GNU and SQL wildcards:
        '*' or '%'  select any amount of characters
        '?' or '_'  select a single character
        
    Terminus supports logical arguments:
        NOT:    By placing '!' in front of the argument, Terminus matches only if the argument is NOT true.
        
            Example: search -y ! 19??, 
            Matches all books in the DB not published in the 1900's

        OR:     By placing 'v' between two values following a flag, you can create queries which a value OR another.

            Example: plot -X year -Y avg pages 100 -y 196? v 197?,
            Plots a graph of the average page count for books in the DB published between 1960 and 1979
            
        AND:    By placing '^' between two values following a flag, you can create queries which a value AND another.
        
            Example: stats -y ! 196? ^ 19?? -g science fiction
            Matches all sci-fi books published in the 1900's but not in 1960's"""

# user selection menu text for set-up.py
SETUP_OPTIONS = """ Set-up Options
        
Create a new user:    [user]
Create a new table:   [table]
Add column to table:  [column]
Open help page:       [help]
Safely exit set-up:   [exit]
"""
        
SETUP_HELP = """Set-up allows for the creation of new attributes for Terminus
    \tEnter command 'user' to start creating a new user
    \tEnter command 'table' to start creating a new table
    \tEnter command 'exit' to safely leave the program
    \tEnter command 'help' to show this page again"""
    
SQLITE3 = """Be sure to have SQLite3 installed on your system.
You can download the latest version at 'https://www.sqlite.org/download.html'
          """
HAS_SQLITE3 = "Do you have SQLite3 installed on this machine? [Y/n]: "

# input prompt text
GET_USER = "Username: "
GET_PW = "Password: "
GET_HOST = "    Host: "

NEW_USER = "Enter new username: "
NEW_PW = "Enter new password: "
CONFIRM_PW = "Confirm new password: "

TABLE = "Table"
NEW_TABLE = "Enter table name:    "
CONFIRM_TABLE = "Confirm table name:  "

END = "end"
REDO = "redo"

COLUMN_TEXT = "Columns\nEnter '" + REDO + "' to restart inputting columns\nEnter '" + END + "' to finish inputting columns\n"

COLUMN_GET = ["Enter column name:   ",
              "Enter datatype:      ",
              "Enter constraint:    "]

# input line indicator for user input without preceding text in set-up.py               
CHEVRON = ">>> "

EXPLAIN1 = """    If new column labels were used that do not exist in statics.FLAGS, add the columns and flag as a key (flag): value (label) pair
    Add to statics.HOST_SET the table name and column list (in order you want them to appear in), as a key (table name): value (column list) pair
    Add to statics.FLAG_HELP the flag name (column label) and help text for that flag, for any new flags created
    Update the statics.HELP_TEXT for 'upload' by appending the table name and column/flag ordering"""
    
EXPLAIN2 = """    Add the columns and flag as a key (flag): value (label) pair if column labels did not previously exist
    Add to statics.HOST_SET the new column to the altered table's list
    Add to statics.FLAG_HELP the flag name (column label) and help text for that flag
    Update the statics.HELP_TEXT for 'upload' by appending column/flag ordering to the altered table
    """

SETUP_MSG = "     System Set-Up"
CLOSE = "\nDatabase connection closed"

# default session variables for clearing the terminal, and setting the terminal window title
CLEAR = "clear"
TERMINAL_TITLE = "title " + VERSION

OTHER_PART =  " in the DB\n\nTo finish the implementation of the table open 'theme.py' perform the following adjustments:\n"

# variables accessable from within terminus scripts
SCRIPT_VARS = {"$trm.weekday": "", "$trm.month": "", "$trm.day": "", "$trm.year": "", "$trm.date": ""}


# print functions which take some variable input
def ret_flag(inpt, i):
    return (inpt[i][1:3] if inpt[i] not in CAPS.keys() else CAPS[inpt[i]]) if len(inpt[i]) > 2 else inpt[i]


# prints message about adjusting theme.py
def adjust(table, adj):
    return "The table '" + table + "' has been " + adj + OTHER_PART


# prints error message for when a non-existent function is called
def funct_err(cmd): return "\nInvalid function '" + cmd + "': enter 'help' for more information."


# prints the first line of the help command's output
def help1(info): return "    " + VERSION + " '" + info + "' supported flags: "


# prints the header for command specific help section
def help2(inpt): return "\n    Command help '" + inpt + "': "
