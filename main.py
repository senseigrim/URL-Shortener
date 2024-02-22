import sqlite3
import os
import string
import random
import webbrowser
import sys

ascii_art = """

 __   __  ______    ___        _______  __   __  _______  ______    _______  _______  __    _  _______  ______   
|  | |  ||    _ |  |   |      |       ||  | |  ||       ||    _ |  |       ||       ||  |  | ||       ||    _ |  
|  | |  ||   | ||  |   |      |  _____||  |_|  ||   _   ||   | ||  |_     _||    ___||   |_| ||    ___||   | ||  
|  |_|  ||   |_||_ |   |      | |_____ |       ||  | |  ||   |_||_   |   |  |   |___ |       ||   |___ |   |_||_ 
|       ||    __  ||   |___   |_____  ||       ||  |_|  ||    __  |  |   |  |    ___||  _    ||    ___||    __  |
|       ||   |  | ||       |   _____| ||   _   ||       ||   |  | |  |   |  |   |___ | | |   ||   |___ |   |  | |
|_______||___|  |_||_______|  |_______||__| |__||_______||___|  |_|  |___|  |_______||_|  |__||_______||___|  |_|

"""

codedb = sqlite3.connect("codes.db")
cursor = codedb.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS codes(code TEXT PRIMARY KEY, url TEXT)")

def create_shortener(link):
    length = 7
    code = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))
    cursor.execute("SELECT code FROM codes")
    codes = cursor.fetchall()
    while (code,) in codes:
        code = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=length))
    
    cursor.execute("INSERT INTO codes (code, url) VALUES (?, ?)", (code, link))
    codedb.commit()
    print(code)
        
def get_link(code):
    cursor.execute("SELECT url FROM codes WHERE code = ?", (code,))
    url = cursor.fetchone()
    if url:
        print(f"URL FOUND: {url[0]}")
        webbrowser.open_new_tab(url[0])
    else:
        print(f"No URL associated with this code.")
        
def get_all_links_and_codes():
    cursor.execute("SELECT code, url FROM codes")
    rows = cursor.fetchall()
    return rows

def reset_database():
    cursor.execute("DELETE FROM codes")
    print("Database reset successful.")
    
def main():
    while True:
        print(ascii_art)
        print("Welcome to URL Shortener")
        print("1. Create Shortener")
        print("2. Get Link from Shortener")
        print("3. Get all shortened URLS")
        print("4. Delete all saved codes.")
        print("0. Exit")
        option = input("Choose an option: ")
        if option == "1":
            link = input("Enter the link: ")
            create_shortener(link)
            input("Press Enter to go back to the menu...")
        elif option == "2":
            code = input("Enter the code: ")
            get_link(code)
            input("Press Enter to go back to the menu...")
        elif option == "3":
            links_and_codes = get_all_links_and_codes()
            for code, link in links_and_codes:
                print(f"Code: {code}, Link: {link}")
            input("Press Enter to go back to the menu...")
        elif option == "4":
            reset_database()
            input("Press Enter to go back to the menu...")
        elif option == "0":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option. Please try again.")
            
if __name__ == "__main__":
    main()


