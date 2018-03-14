#!/usr/bin/python3
import session
import query
import theme


def format_quote(quote):
    """Formats quotes which trail multiple lines by inserting newlines between words.
    Otherwise, lines will often be split mid word.""" 
    barrier = theme.WIDTH - theme.BOUNDS
    length = len(quote)

    while barrier < length:
        for i in range(theme.BOUNDS):
            if barrier+i < len(quote) and quote[barrier+i] == " ":
                quote = quote[:barrier+i] + "\n " + quote[barrier+i:]
                break

        barrier += theme.WIDTH - theme.BOUNDS

    return quote


def random_quote(db):
    """Randomly selects/prints one quote from the quotes table."""
    quote = db.cursor()
    quote.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    row = quote.fetchone()
    
    if row is not None:
        print("\n \"" + format_quote(row[3]) + "\"\n\n\t-" + row[1] + "\n\t " + row[0] + ", " + str(row[2]))
    
    quote.close()


def home_screen(db):
    """Prints the start screen, and random quote."""
    print(theme.TITLE)

    random_quote(db)
    input(theme.PAUSE)
    session.clear_screen()


def main():
    """Landing point, sets info variables used through the program.
    Transfers control to the function which takes command input"""
    session.title()
    session.clear_screen()
    
    # info[0] = sqlite DB connection
    # info[1] = current host table
    # info[2] = user name (for printing the command prompt)
    info = [None, None, None]
    info[0] = session.get_connection()
    home_screen(info[0])
    # sets info variables used throughout active session
    info[1], info[2] = session.login(info[0])
    
    query.landing(info)
    session.clear_screen()
    exit()


if __name__ == '__main__':
    session.system_vars()
    main()
