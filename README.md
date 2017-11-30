# Terminus: Terminal Library Database
The third iteration of the terminal based library database. Unlike the previous java versions this one is written in python.
With each iteration, I have overhauled the interface style. Terminus is a pure bash experience. 
Flags are finally supported rather than weird file path syntax: python was chosen to make flag processing easier.
The previous versions had, to varying degrees of severity, input syntax dissonance where no truly uniform command input syntax existed. 
The input syntax has now been unified under the comfortable, user friendly, flag style.
Unlike the previous versions, Terminus was designed to be table scalable. 
In previous versions it would have been a nightmare to integrate new table into the system; however, now it's fairly straight forward.

# Features
- 3 library host tables (books, stories, quotes), and 1 administrative host table (records)
- 13 command functions including: file upload, the aggregate trinity, query result export...
- User/password system
- Full wildcard support
- Case insensitive searching
- 8 data points for 'books', 6 data points for 'stories', 4 data points for 'quotes', and 5 data points for 'records'
- The Litany Against Fear

# Initial Set-up
- Download files, create a directory for Terminus (consider creating a desktop shortcut to one of the start-up scripts)
- Make sure you have sqlite3 installed on your machine (https://www.sqlite.org/download.html)
- Run set-up.py from terminal, it will prompt you to create a new user
- Create a CSV of your current library using the expected column ordering format (title, author, genre, year, pages, type, format, finished).
Beware of single quotes, SQL syntax expects two single quotes ('') in the place of a one single quote (')
- Execute an 'upload' command

# General Use
Either run python3 terminus.py, or one of the scripts to launch the program. 
Enter the username/password you created in the initial set-up. Begin normal use.

# Command List
- search, searches the current host table. The flag inputs constitute the SQL WHERE clause.

      user@host: search -a Harlan Ellison -T short stories
- insert, inserts a new record into the host table. Currently, it's not flag order specific, run 'help insert' for more information.

      user@host: insert -t Labryinths -a Jorge Luis Borges -g sf -y 1962 -p 251 -T stories -f paperback -F false
- remove, deletes records from host table. The flag inputs constitute the SQL WHERE clause.

      user@host: remove -t Man Plus
- complete, sets the 'finished' column to true. The flag inputs constitute the SQL WHERE clause.

      user@host: complete -t The Big Time
- sum, performs the SQL SUM aggregation.

      user@host: sum pages -t short stories
- count, performs the SQL COUNT aggregation.

      user@host: count titles -F true
- average, performs the SQL AVG aggregation.

      user@host: average year -g science fiction
- change, allows user to change host table, or change user entirely.

      user@host: change -h short stories -u test_user pw1234
- upload, performs a file upload from CSV to the current host table.

      user@host: upload /directory/path/test_upload.csv
- stats, outputs a statistics table for a search query. All agruments are processed as a 'search' command.

      user@host: stats -F true
- export, writes the output of both a 'search' and 'stats' call to a file (named 'd/m/y DB Export.txt'). 
All arguments are processed as a 'search' command.
        
	  user@host: export -T stories -g science fiction -s author
- help, displays general and host specific use information. 'help command_here' includes use information for that command.

      user@host: help upload
- exit, safely leaves Terminus

      user@host: exit
   
# Column/Flags
'books' host table has 8 columns: title (-t), author (-a), genre (-g), year (-y), pages (-p), type (-T), format (-f), finished (-F)

'stories' host table has 6 columns: title (-t), author (-a), genre (-g), year (-y), pages (-p), collection (-c), finished (-F)

'quotes' host table has 4 columns: title (-t), author (-a), year (-y), quote (-q)

'reocrds' host table has 5 columns: date (-d), user (-u), operation (-o), host (-h), arguments (-A)

Type column/flag denotes whether the books is a novel, short stories...

Format column/flag denotes whether the book is paperback or hardcover

Finished column/flag denotes whether you have finished the book

Collection column/flag denotes the short story colleciton the story comes from

# Integrating a New Table
- Open library.db in sqlite3, add the new table
- If new column labels were used that do not exist in statics.py, include them in 'FLAGS' and 'ALL_COLUMNS'
- With the new column, update the dictionary 'HOST_SET' in statics.py
- Describe any new column in the 'FLAGS_HELP' dictionary in statics.py
- Finally update the upload section in 'HELP_TEXT' dictionary in statics.py
