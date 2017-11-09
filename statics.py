PAUSE = "\nPress Enter to continue..."

FLAGS = {"-a": "Author", "-t": "Title", "-g": "Genre", "-T": "Type",
         "-y": "Year", "-p": "Pages", "-f": "Format", "-F": "Finished", 
         "-c": "Collection", "-q": "Quote", "-d": "Date", "-o": "Operation",
         "-h": "Host", "-u": "User", "-A": "Arguments"}

ALL_COLUMNS = ["Title", "Author", "Genre", "Year",
               "Pages", "Type", "Format", "Finished",
               "Collection", "Quote", "Date", "Operation",
               "Arguments", "Host", "User"]

HOST_SET = {"books": ["Title", "Author", "Genre", "Type", "Year", "Pages", "Format", "Finished"],
            "stories": ["Title", "Author", "Genre", "Year", "Pages", "Finished", "Collection"],
            "quotes": ["Title", "Author", "Year", "Quote"],
            "records": ["Date", "User", "Operation", "Host", "Arguments"]}
            
VERSION = "Terminus vDEV"

WIDTH = 125
BOUNDS = 30
HEIGHT = 30
