PAUSE = "\nPress Enter to continue..."

FLAGS = {"-a": "Author", "-t": "Title", "-g": "Genre", "-T": "Type",
         "-y": "Year", "-p": "Pages", "-f": "Format", "-F": "Finished", 
         "-c": "Collection", "-q": "Quote", "-d": "Date", "-o": "Operation",
         "-h": "Host", "-u": "User", "-A": "Arguments"}

ALL_COLUMNS = ["Title", "Author", "Genre", "Year",
               "Pages", "Type", "Format", "Finished",
               "Collection", "Quote", "Date", "Operation",
               "Arguments", "Host", "User"]

HOST_SET = {"books": ["Title", "Author", "Genre", "Year", "Pages", "Type", "Format", "Finished"],
            "stories": ["Title", "Author", "Genre", "Year", "Pages", "Finished", "Collection"],
            "quotes": ["Title", "Author", "Year", "Quote"],
            "records": ["Date", "User", "Operation", "Host", "Arguments"]}
            
VERSION = "Terminus v1.0"

WIDTH = 125
BOUNDS = 35
HEIGHT = 30

HELP = """    Terminus supports 10 flags:
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
        -s or --sort        flag specifies the sorting column: sort is supported by insert and aggregate only
        -d or --date        flag specifies the date in day/mon/year hr:mi:sc
        -u or --user        flag specifies the user
        -o or --operation   flag specifies the operation used
        -h or --host        flag specifies the host
        -A or --arguments   flag specifies the command arguments
        
    Flag support by host:
        books:      -t, -a, -g, -y, -p, -T, -f, -F
        stories:    -t, -a, -g, -y, -p, -c
        quotes:     -t, -a, -y, -q
        records:    -d, -u, -o, -h, -A
        
    Command list:
        search      perform SELECT SQL function
        insert      performs INSERT INTO SQL function
        remove      performs DELETE SQL function
        complete    performs UPDATE SQL function (only changes finished column to 'true')
        aggregate   performs AVG, SUM, and COUNT SQL functions
        change      allows host table and user change
        upload      allows for bulk insert from CSV file
        exit        safely exits program
        
    Terminus supports both GNU and SQL wildcards:
        '*' or '%'  select any amount of characters
        '?' or '_'  select a single character"""

SEARCH = """
    Example: search -a Harlan Ellison -T short stories"""

INSERT = """
    Flag order is important for insert
    Example: insert -t Labryinths -a Jorge Luis Borges -g sf -y 1962 -p 251 -T short stories -f paperback -F false"""

REMOVE = """
    Example: remove -t Man Plus"""

COMPLETE = """
    Example: complete -t A Scanner Darkly"""

AGGREGATE = """
    Aggregate has three additional flags:
        -cnt or --count     COUNT SQL function
        -sum or --sum       SUM SQL function
        -avg or --average   AVG SQL function
        
    Example: aggregate -cnt title -T short stories
    Count the title column where the type is 'short stories'"""

CHANGE = """
    Change has two additional flags:
        -h or --host    specifies name of new host table
        -u or --user    takes two arguments following the flag: username password
        
    Example: change -h short stories -u test_user pw1234"""

UPLOAD = """
    Upload takes no flag arguments, and file must be a csv with no column labels
    
    Expected column ordering by host table:
        books:      -t, -a, -g, -y, -p, -T, -f, -F
        stories:    -t, -a, -g, -y, -p, -c, -F
        quotes:     -t, -a, -y, -q
        records:    -d, -u, -o, -h, -A
        
    Example: upload /path/to/file/if/not/in/curr/directory/test_upload.csv
    If an item in the upload has a column value with a comma, insert that item individually"""

EXIT = """
    Exit takes no arguments used to safely leave the program"""

TEXT = {"search": SEARCH, "insert": INSERT, "remove": REMOVE,
        "complete": COMPLETE, "aggregate": AGGREGATE, "change": CHANGE,
        "upload": UPLOAD, "exit": EXIT}
