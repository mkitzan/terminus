# Terminus: Terminal Library Database
This is the third iteration of the terminal based library database. Unlike the previous java versions this iteration is written in python.
With each iteration, I have overhauled the interface style. Terminus is a pure bash styled experience. 
Flags are finally supported rather than weird file path syntax: python was chosen to make flag processing easier.
The previous versions had, to varying degrees of severity, command syntax dissonance, where no truly uniform syntax existed. 
The input syntax has now been unified under the comfortable, user friendly, flag style. 
Unlike the previous versions, Terminus was designed to be table, and column scalable. 
In previous versions it would have been a nightmare to integrate new table into the system; however, now it's fairly straight forward. Implementing a new column or table involves adding values to datastructures in the the theme file ('theme.py'), and performing SQL operations to add the table or column.

# Issues?
If you have any issues setting Terminus up, using it, or run into bugs, please leave an issue in that tab of the repo. I'm happy to answer or fix any issues which occur. No current issue submission format exists. If it's a bug include the terminal output, so I can locate the problem line. If it's a set-up / use issue, please describe in detail the problem arrisen using vocabulary from the help pages or this readme (if none exist to describe your issue, then go for whatever).

# Features
- 4 library host tables (books, stories, quotes, wishlist), and 3 administrative host table (tracker, records, planner)
- 19 command functions including: file upload, plot graphical query output, the aggregate trinity, query result export, scripting...
- User/password system
- Full wildcard support
- Case insensitive searching
- 8 cols for 'books', 6 cols for 'stories', 4 cols for 'quotes', 7 cols for 'wishlist', 6 cols for 'tracker', 5 cols for 'planner', and 5 cols for 'records'
- The Litany Against Fear

# Initial Set-up
- Download files, create a directory for Terminus (consider creating a desktop shortcut to one of the start-up scripts)
- Make sure you have sqlite3 installed on your machine (https://www.sqlite.org/download.html)
- Run setup.py from a terminal, it will allow you to create a new user
- Create a CSV or TSV of your current library using the expected column ordering format (title, author, genre, year, pages, type, format, finished)
- Execute an 'upload' command

# General Use
Either run python3 source/terminus.py, or one of the scripts to launch the program. 
Enter the username/password you created in the initial set-up. Begin normal use.

# Command List
- search, searches the current host table. The flag inputs constitute the SQL WHERE clause.

      user@host: search -a Harlan Ellison -T short stories
- insert, inserts a new record into the host table. Currently, it's not flag order specific, run 'help insert' for more information.

      user@host: insert -t Labryinths -a Jorge Luis Borges -g sf -y 1962 -p 251 -T stories -f paperback -F false
- remove, deletes records from host table. The flag inputs constitute the SQL WHERE clause.

      user@host: remove -t Man Plus
- update, allows user to change field of a record. The flag inputs constitute the SQL WHERE clause.

      user@host: update type stories -t City
- sum, performs the SQL SUM aggregation.

      user@host: sum pages -t short stories
- count, performs the SQL COUNT aggregation.

      user@host: count titles -F true
- average, performs the SQL AVG aggregation.

      user@host: average year -g science fiction
- plot, prints a simple graph of an aggregated query.
Each axis flag has a DB column specified, and one of those two states the aggregate type and the scale to plot by.

      user@host: plot -X author -Y count title 1 -F true
- change, allows user to change host table, or change user entirely.

      user@host: change -h short stories -u test_user pw1234
- distinct, performs the function of a SQL SELECT DISTINCT.
Distinct value column is stated directly next to the 'distinct' command word.

      user@host: distinct title -C search -F true -s author
- upload, performs a file upload from a CSV or TSV file to the current host table.

      user@host: upload /directory/path/test_upload.csv
- stats, outputs a statistics table for a search query. All arguments are processed as a 'search' command.

      user@host: stats -F true
- report, writes the output of 'search', 'stats', and 'plot' calls to a file (named 'd/m/y Library Export.txt'). 
All arguments are processed as a 'search' command.
        
      user@host: report -T stories -g science fiction -s author
- script, allows user to exceute a Terminus script (.trm). 
Any script variable must be declared in the script command arguments, and inside the script a variable call must be preceded by '$'.
Look at the example script 'complete.trm' in the scripts folder.

      user@host: script -S complete.trm title=Sturgeon is Alive and Well...
- sql, allows user to execute a raw SQL statement. The statement can't query sqlite_master nor credentials.
Must declare either 'search', 'stats', and 'tsv' as the first argument.

      user@host: sql search SELECT title, author, year FROM books UNION SELECT title, author, year FROM stories
- export, allows user to export a query as a tsv file for use in other programs or applications.

      user@host: export -F false -T ! manga ^ ! art book
- system, allows user to create new DB objects from within the program.
Applicable DB objects include new tables, users, columns (for existing tables).

	  user@host: system user table
- help, prints the general help page, and specific help pages for all the following arguments.
      
      user@host: help upload plot search
- exit, safely leaves Terminus

      user@host: exit
   
# Column/Flags
'books' host table has 8 columns: title (-t), author (-a), genre (-g), year (-y), pages (-p), type (-T), format (-f), finished (-F)

'stories' host table has 6 columns: title (-t), author (-a), genre (-g), year (-y), pages (-p), collection (-c), finished (-F)

'quotes' host table has 4 columns: title (-t), author (-a), year (-y), quote (-q)

'wishlist' host table has 7 columns: title (-t), author (-a), genre (-g), year (-y), pages (-p), type (-T), priority (-P)

'tracker' host table has 6 columns: weekday (-w), month (-m), day (-d), year (-y), title (-t), pages (-p)

'planner' host table has 5 columns: month (-m), year (-y), title (-t), author (-a), pages (-p)

'records' host table has 5 columns: date (-D), user (-u), operation (-o), host (-h), arguments (-A)

Type column/flag denotes whether the books is a novel, short stories...

Format column/flag denotes whether the book is paperback or hardcover

Finished column/flag denotes whether you have finished the book

Collection column/flag denotes the short story collection the story comes from

# Integrating a New Table
- Open setup.py from within a terminal, and enter 'table' at the chevrons
- Alternatively, enter 'system table' from within Terminus itself
- Enter and confirm the new table name
- Enter as many column label, data type, constraints as needed
- If new column labels were used that do not exist in 'statics.py', include them in 'FLAGS'
- Add the new table's name, and column names (in order) into HOST_SET, as a key (table name):value (list of columns) pair
- Describe any new column in the 'FLAG_HELP' dictionary in statics.py
- Finally update the upload section in 'HELP_TEXT' dictionary in statics.py by appending the table and column flags to the table
