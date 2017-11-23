VERSION = "Terminus v1.2"

WIDTH = 125
BOUNDS = 35
HEIGHT = 35

PAUSE = "\nPress Enter to continue..."

FLAGS = {"-a": "Author", "-t": "Title", "-g": "Genre", "-T": "Type",
         "-y": "Year", "-p": "Pages", "-f": "Format", "-F": "Finished", 
         "-c": "Collection", "-q": "Quote", "-d": "Date", "-o": "Operation",
         "-h": "Host", "-u": "User", "-A": "Arguments"}

HOST_SET = {"books": ["Title", "Author", "Genre", "Year", "Pages", "Type", "Format", "Finished"],
            "stories": ["Title", "Author", "Genre", "Year", "Pages", "Collection", "Finished"],
            "quotes": ["Title", "Author", "Year", "Quote"],
            "records": ["Date", "User", "Operation", "Host", "Arguments"]}

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

HELP_TEXT = {"search": """        Example: search -a Harlan Ellison -T short stories""", 
             "insert": """        Flag order is important for insert
        Example: insert -t Labryinths -a Jorge Luis Borges -g science fiction -y 1962 -p 251 -T short stories -f paperback -F false""", 
             "remove": """        Example: remove -t Man Plus""",
             "complete": """        Example: complete -t A Scanner Darkly""", 
             "sum": """        Example: sum pages -T short stories""", 
             "count": """        Example: count title -F true""",
             "average": """        Example: average year -g science fiction""", 
             "change": """        Change has two additional flags:
            -h or --host    specifies name of new host table
            -u or --user    takes two arguments following the flag: username password
            
        Example: change -h short stories -u test_user pw1234""", 
             "upload": """        Upload takes no flag arguments, and file must be a csv with no column label row
        
        Expected column ordering by host table:
            books:      -t, -a, -g, -y, -p, -T, -f, -F
            stories:    -t, -a, -g, -y, -p, -c, -F
            quotes:     -t, -a, -y, -q
            records:    -d, -u, -o, -h, -A
            
        Example: upload /file/path/if/not/in/curr/directory/test_upload.csv
        If an item in the upload has a column value with a comma, insert that item individually""", 
             "stats": """        Stats produces a table of statistics for a search query. All agruments are processed as a 'search' command.
        Statistics table includes a row count, unique item count, sum, average, standard deviation, minimum, and maximum.

        Example: stats -g science fiction -y 19??""",
             "exit": """        Exit takes no arguments used to safely leave the program"""}

HELP_STANDARD = """
    Command list:
        search      perform SELECT SQL function
        insert      performs INSERT INTO SQL function
        remove      performs DELETE SQL function
        sum         performs SUM SQL function
        count       performs COUNT SQL function
        average     performs AVG SQL function
        complete    changes finished column to 'true'
        stats       outputs a statistics table on a 'search' command
        change      allows host table and user change
        upload      allows for bulk insert from CSV file
        exit        safely exits program
        
    Terminus supports both GNU and SQL wildcards:
        '*' or '%'  select any amount of characters
        '?' or '_'  select a single character"""

