VERSION = "Terminus v2.2"

# font BIG, two spaces between name and ver: http://patorjk.com/software/taag/#p=display&f=Big&t=Terminus%20%20v2.3
TITLE = """
      _______                  _                         ___    ___  
     |__   __|                (_)                       |__ \  |__ \ 
        | | ___ _ __ _ __ ___  _ _ __  _   _ ___   __   __ ) |    ) |
        | |/ _ \ '__| '_ ` _ \| | '_ \| | | / __|  \ \ / // /    / / 
        | |  __/ |  | | | | | | | | | | |_| \__ \   \ V // /_ _ / /_ 
        |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|___/    \_/|____(_)____|
     Terminal Library Database
    """

DB = "library.db"
DEFAULT_HOST = "books"

WIDTH = 125
BOUNDS = 35
HEIGHT = 35
PROGRESS = 35

# error and pause text
PAUSE = "\nPress enter to continue..."
HOST_ERROR = "\nInvalid host input"
LOGIN_ERROR = "\nInvalid login credentials"
CMD_ERROR = "        Invalid command"
EXCEPT = "\nTry: help "

# logic ops available in queries
LOGIC_OPS = {"v": [-1, "' OR "], "^": [-1, "' AND "], "!": [-3, " NOT "]}

# names of tables, not allowed to be accessed
BLOCKED = ["sqlite_master", "credentials"]

PARSE = {"remove": lambda h: "DELETE FROM " + h}

# flag and column pairs for all columns throughout the DB
FLAGS = {"-a": "Author", "-t": "Title", "-g": "Genre", "-T": "Type",
         "-y": "Year", "-p": "Pages", "-f": "Format", "-F": "Finished", 
         "-c": "Collection", "-q": "Quote", "-d": "Date", "-o": "Operation",
         "-h": "Host", "-u": "User", "-A": "Arguments"}
        
# all flags with capital short flags
CAPS = {"--type": "-T", "--finished": "-F", "arguments": "-A"}

# list of columns for each table (in order)
HOST_SET = {"books": ["Title", "Author", "Genre", "Year", "Pages", "Type", "Format", "Finished"],
            "stories": ["Title", "Author", "Genre", "Year", "Pages", "Collection", "Finished"],
            "quotes": ["Title", "Author", "Year", "Quote"],
            "records": ["Date", "User", "Operation", "Host", "Arguments"]}

# help text for each flag/column
FLAG_HELP = {"Title": "        -t or --title       flag specifies the title",
             "Author": "        -a or --author      flag specifies the author",
             "Genre": "        -g or --genre       flag specifies the genre",
             "Year": "        -y or --year        flag specifies the publishing year",
             "Pages": "        -p or --pages       flag specifies the page number",
             "Type": "        -T or --type        flag specifies the type of book ie novel, short stories...",
             "Format": "        -f or --format      flag specifies the book format ie paperback, hardcover...",
             "Finished": "        -F or --finished    flag specifies whether the book's been finished",
             "Collection": "        -c or --collection  flag specifies a short story's collection",
             "Quote": "        -q or --quote       flag specifies a book quote",
             "Date": "        -d or --date        flag specifies the date in day/mon/year hr:mn:sc",
             "User": "        -u or --user        flag specifies the user",
             "Operation": "        -o or --operation   flag specifies the operation used",
             "Host": "        -h or --host        flag specifies the host",
             "Arguments": "        -A or --arguments   flag specifies the command arguments"}

# help text for each command function
HELP_TEXT = {"search": """        Example: search -a Harlan Ellison -T short stories""", 
             "insert": """        Flag order is not important for insert; however, all flags must be present
        Example: insert -t Labryinths -a Jorge Luis Borges -g science fiction -y 1962 -p 251 -T stories -f paperback -F false""", 
             "remove": """        Example: remove -t Man Plus""",
             "update": """        Update the first argument states the column where the update will take place, the next set states the change to be made
        Finally, the last set ('-t A Scanner Darkly' in the example) states the where clause the perform the update by
        
        Example: update finished true -t A Scanner Darkly""", 
             "sum": """        Example: sum pages -T short stories""", 
             "count": """        Example: count title -F true""",
             "average": """        Example: average year -g science fiction""", 
             "change": """        Change has two additional flags:
            -h or --host    specifies name of new host table
            -u or --user    takes two arguments following the flag: username password
            
        Example: change -h short stories -u test_user pw1234""", 
             "plot": """        Plot prints a simple graph of an aggregated query
        Each axis flag needs a DB column specified, and one of those two states the aggregate type and the scale to plot by
        All non-axis arguments are interpreted in the standard 'search' format
        
        Example: plot -X author -Y count title 1 -g science fiction -F true""",
             "upload": """        Upload takes no flag arguments, and file must be a csv with no column label row
        
        Expected column ordering by host table:
            books:      -t, -a, -g, -y, -p, -T, -f, -F
            stories:    -t, -a, -g, -y, -p, -c, -F
            quotes:     -t, -a, -y, -q
            records:    -d, -u, -o, -h, -A
            
        Example: upload /directory/path/test_upload.csv
        If an item in the upload has a column value with a comma, insert that item individually""", 
             "stats": """        Stats produces a table of statistics for a search query. All arguments are processed as a 'search' command.
        Statistics table includes a row count, unique item count, sum, average, standard deviation, minimum, and maximum

        Example: stats -g science fiction -y 19??""",
             "export": """        Export writes the output of both a 'search' and 'stats' call to a unique file. 
        All arguments are processed as a 'search' command
        
        Example: export -T stories -g science fiction -s author""",
             "distinct": """        Distinct allows for searching records with the distinct values in the specified column
        Specific column is stated directly next to the 'distinct' command word
        Unique flag '-C' or '--command' states how to run the arguments. Commands: 'search', 'stats', 'tsv', and 'export'
        
        Example: distinct title -F true -s author -C search""",
             "sql": """        The SQL command allows user to enter a raw SQL query. Useful for JOIN queries.
        The user must declare, immediately after the 'sql' keyword, either 'search' or 'stats'.
             
        Example: sql search SELECT Author, Year FROM books WHERE Year LIKE 19%%""",
             "tsv": """        Exports a TSV file of a search query. Useful when using library data for other programs.
             
        Example: tsv -F false""",
             "exit": """        Exit takes no arguments. Used to safely leave the program"""}

# default help text
HELP_STANDARD = """
    Command list:
        search      performs SELECT SQL function
        distinct    performs SELECT DISTINCT SQL function
        insert      performs INSERT INTO SQL function
        remove      performs DELETE SQL function
        sum         performs SUM SQL function
        count       performs COUNT SQL function
        average     performs AVG SQL function
        update      performs the UPDATE SQL function
        plot        prints a simple graph of an aggregated query
        stats       outputs a statistics table on a 'search' command
        change      allows host table and user change
        upload      allows for bulk 'insert' from CSV file
        export      allows writing query output to a text file
        sql         allows user to enter a raw SQL query
        tsv         allows user to export data for use in other applications
        exit        safely exits program
        
    Terminus supports both GNU and SQL wildcards:
        '*' or '%'  select any amount of characters
        '?' or '_'  select a single character
        
    Terminus supports logical arguments:
        NOT:    By placing '!' in front of the argument, Terminus matches only if the argument is NOT true.
        
            Example: search -y ! 19??, 
            Matches all books in the DB published in the 1900's

        OR:     By placing 'v' between two values following a flag, you can create queries which a value OR another.
        
            Example: plot -X year -Y avg pages 100 -y 196? v 197?,
            Plots a graph of the average page count for books in the DB published between 1960 and 1979
            
        AND:    By placing '^' between two values following a flag, you can create queries which a value AND another.
        
            Example: stats -y ! 196? ^ 19?? -g science fiction
            Matches all sci-fi books published in the 1900's but not in 1960's"""

SETUP_OPTIONS = """ Set-up Options
        
Create a new user:    [user]
Create a new table:   [table]
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

SETUP_MSG = "     System Set-Up"
CLOSE = "\nDatabase connection closed"

CLEAR = "clear"
TERMINAL_TITLE = "title " + VERSION

# print functions which take some variable input
def ret_flag(inpt, i):
    return (inpt[i][1:3] if inpt[i] not in CAPS.keys() else CAPS[inpt[i]]) if len(inpt[i]) > 2 else inpt[i]


def funct_err(cmd): return "\nInvalid function '" + cmd + "': enter 'help' for more information."


def help1(info): return "    " + VERSION + " '" + info + "' supported flags: "


def help2(inpt): return "\n    Command help '" + inpt + "': "
