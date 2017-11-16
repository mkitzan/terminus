#!/usr/bin/python3
import session
import query
import statics


def format_quote(quote):
    barrier = statics.WIDTH-statics.BOUNDS
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
    #font BIG, two spaces between name and ver: http://patorjk.com/software/taag/#p=display&f=Big&t=
    print("""
     _______                  _                         __   ___  
    |__   __|                (_)                       /_ | / _ \ 
       | | ___ _ __ _ __ ___  _ _ __  _   _ ___   __   _| || | | |
       | |/ _ \ '__| '_ ` _ \| | '_ \| | | / __|  \ \ / / || | | |
       | |  __/ |  | | | | | | | | | | |_| \__ \   \ V /| || |_| |
       |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|___/    \_/ |_(_)___/       
    Terminal Library Database
    """)

    random_quote(db)
    input(statics.PAUSE)
    session.clear_screen()


def main():
    session.title()
    session.resize()
    session.clear_screen()

    info = [None, None, None]
    info[0] = session.get_connection()

    home_screen(info[0])

    info[2] = session.change_user(info[0])
    info[1] = session.change_host(info[0])
    
    query.landing(info)
    session.clear_screen()
    exit()


if __name__ == '__main__':
    main()
