#!/usr/bin/python3
import session
import query
import statics


def format_quote(quote):
    barrier = statics.WIDTH - statics.BOUNDS
    length = len(quote)

    while barrier+statics.BOUNDS < length:
        for i in range(statics.BOUNDS):
            if quote[barrier+i] == " ":
                quote = quote[:barrier+i] + "\n " + quote[barrier+i:]
                break

        barrier += statics.WIDTH-(statics.BOUNDS-20)

    return quote


def random_quote(db):
    quote = db.cursor()
    quote.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    row = quote.fetchone()
    
    if row is not None:
        print(" \"" + format_quote(row[3]) + "\"\n\t-" + row[1] + "\n\t " + row[0] + ", " + str(row[2]))
    
    quote.close()


def home_screen(db):
    print(statics.TITLE)

    random_quote(db)
    input(statics.PAUSE)
    session.clear_screen()


def main():
    session.title()
    session.clear_screen()
    
    info = [None, None, None]
    info[0] = session.get_connection()

    home_screen(info[0])

    info[1], info[2] = session.login(info[0])
    
    query.landing(info)
    session.clear_screen()
    exit()


if __name__ == '__main__':
    session.system_vars()
    main()
