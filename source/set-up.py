import session
import getpass


def get_user():
    match = False
    
    while not match:
        session.clear_screen()
        user = input("Enter new username: ")
        password = getpass.getpass("Enter new password: ")
        confirm = getpass.getpass("Confirm new password: ")
    
        match = True if password == confirm else False

    return user, password
    

def main():
    print("Be sure to have SQLite3 installed on your system\n"
          "You can download the latest version at \"https://www.sqlite.org/download.html\"\n")
    check = input("Do you have SQLite3 installed on system? [Y/n]: ")
    
    if check.lower() == "n":
        exit()

    user, password = get_user()
    session.new_user([user, password], session.get_connection())


if __name__ == "__main__":
    main()
