
from app_functions import close_connection, connect, insert_values, attempt_login, account_exists, is_valid_email, is_valid_faculty, is_valid_name, attempt_signup, get_user_action, login_or_signup, penalty_list, user_penalty_payment, choose_signout_option, get_members, return_book_table_stats, offer_to_return_book, offer_to_write_review, search_book, borrow_book, getBook, display
import sqlite3 
import sys

################# HELPER FUNCTIONS/MAIN FUNCTIONS(CAN BE TURNED INTO A HEADER FILE ONCE ALL FUNCTIONS ARE IMPLEMENTED/TESTED)######################    


def main():
    if len(sys.argv) != 2:
        print("Usage: python my_script.py <db_file>")
        sys.exit(1)

    path = sys.argv[1]
    #print(f"DB file path: {path}")
    #Done So Far: implemented insertion function and user action prompt function
    connect(path)#creates a connection to the DB
    # allows further functionalities once the login/signup has been handled         
    # creates the logical sequence of the code
    # must ensure that the user can quit from the program at any given time
    user_choice = None
    # email = login_or_signup()#prompts the user to login or signup for the website
    while user_choice != 'quit':
        email = login_or_signup()#prompts the user to login or signup for the website
        current_user = email
        print(f'\nCurrent user: {email}\n')
        assert current_user != None
        display(email)

    
    
    

    close_connection()
    return

if __name__ == "__main__":
    main()
    
