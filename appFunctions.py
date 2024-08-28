import sqlite3 
import sys
import getpass
from datetime import datetime
from datetime import date

from random import randint

connection = None
cursor = None


def close_connection():
    connection.commit()
    connection.close()
    
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

#Inserts values into the DB

def insert_values(table: str, data)-> bool: # returns false if the insertion fails, true otherwise
    global connection, cursor
    # holds a dictionary with all of the table name and their respective columns, used for inserting values into a relation
    tables = ["members","books","borrowings","penalties","reviews"]
    if table in tables:
        insert_value : str = f"INSERT INTO {table} VALUES {data};"# tables[table] corresponds to the structure of a given table which is being inserted into
        #for testing
            
        #print(f"Attempting to {insert_value}\n")
        try: 
            cursor.execute(insert_value)
            connection.commit()
        #for testing:
            #print(f"Transaction: '{insert_value}' Completed Successfully\n")
        # see the current contents of the table being inserted into, for testing
            cursor.execute("SELECT * FROM members")
            tuples = cursor.fetchall()
            connection.commit()
            #for test values, comment out if not needed
            #print(f"Current members table: {tuples}")
            return True 
        except:  
            print("Insertion failed, format incorrect or constraints not met. Make sure to drop previous tables before running the python code.")
            return False
    else: 
        print("Cannot complete insertion, this is not a valid table")
    return False

def attempt_login(): # returns what the result of the login is, returns a string of the email upon a successful login
    # prompts the user to login
    global connection, cursor
    user_info = None
    while user_info == None:
        # lets user return the the login screen by typing escape, gives them a quitting choice
        print("\n***Enter 'escape' at anytime to return to the login/registration screen***")
        
        # typing escape at any point allows the user to return to the login screen, returns 'terminated' to indicate a terminated login
        email = input("Please Enter Your Email Address:\n> ")
        if email.lower() == 'escape':
            return 'terminated'
        elif account_exists(email):
            password = getpass.getpass("Please Enter Your Password:\n> ")
            if password.lower() == 'escape':
                return 'terminated'
            
            cursor.execute ('SELECT * FROM members WHERE email = LOWER(?) AND passwd = ?;',(email, password),)
            user_info = cursor.fetchone()

            if user_info is not None and len(user_info[2]) > 0:
                #connection.commit()
                
                #means successful login, returns the email if the login succeeds and returns it in a variable
                return email 

            else:
                return False #means failed login
        else:
            print("\nThere is no account with this email address in our records.")
    

def account_exists(email:str) -> bool:
    global connection, cursor
    # checks if an email already exists for a user in the database
    cursor.execute(f"SELECT email FROM members WHERE email = '{email}'")
    result = cursor.fetchone()
    if result is not None and result[0] == email:
        #connection.commit() # WHY???
        return True
    else:
        print(result)
        return False
    
    
def is_valid_faculty(faculty:str) -> bool:
    # checks that the name entered by the user is valid, informs the user of all aspects of the name that need to be altered
    if faculty != None and faculty != '' and len(faculty) <= 100:
    
        # checks that the faulty name has at least one non-space character 
        for character in faculty:
            if character != ' ':
            
             return True
         
        else:
            # If there are no non-space characters, it is indicated to the user and they are prompted to enter a proper email
            print("\nYour faculty name must contain at least one non-space character")
            return False
            
    if faculty == None:
        print("Your faculty name cannot be empty")
    elif faculty != None and len(faculty) > 100:
        print("Your faculty name must be less than 255 characters long\n")
    
    return False

def is_valid_name(name:str) -> bool:
    # checks that the name entered by the user is valid, informs the user of all aspects of the name that need to be altered
    if name != None and len(name) <= 255:
        # firsly checks that the name has no spaces
        for character in name:
            if character == ' ':
                print(f"\nThe name '{name}' is invalid, you cannot have spaces in your name")
                return False
        # once it has been checked that the name has no spaces, it is ensured that the name has at least one non-space character 
        for character in name:
            if character != '':
                return True
         
        # If there are no non-space characters, it is indicated to the user and they are prompted to enter a proper email
        print("\nYour name must contain at least one non-space character")
            
        return False
    if name == None:
        print("Your name cannot be empty")
    elif name != None and len(name) > 255:
        print("Your name must be less than 255 characters long\n")
    
    return False

def is_valid_email(email:str) -> bool:
    # checks that the email entered by the user is valid, informs the user of all aspects of the name that need to be altered
    # same logic as is_valid_name but with different constraints
    if email != None and len(email) <= 100:

         # firsly checks that the email has no spaces

        for character in email:
            if character == ' ':
                print(f"\nThe email '{email}' is invalid, you cannot have spaces in your email.")
                return False
        # once it has been checked that the email has no spaces, it is ensured that the name has at least one non-space character 
        for character in email:
            if character != '':
                return True
        # If there are no non-space characters, it is indicated to the user and they are prompted to enter a proper email
        print("\nYour email must contain at least one non-space character.")
        return False
    if email == None: 
        print("Your email cannot be empty")
    elif email != None and len(email) > 100:
        print("Your email must be less than 255 characters long.\n")

    return False
    
    
def attempt_signup() -> str:# returns the result of the sign up attempt: 'terminated' if the user exits during signup, 'successful' if the signup succeeds
    global connection, cursor
    # attempts to sign a user up in the database
    signed_up = False # flag that turns to true once a successful signup has taken place
    
    # lets user return the the login screen by typing escape, gives them a quitting choice
    print("\n***Enter 'escape' after any prompt to return to the login/registration screen***")
    
    while not signed_up: 
        
        valid_email = False # flag that turns to true once a valid email has been entered into the program
        while not valid_email:
            email = input("Please enter the email you would like to use (entering 'escape' will return you to the login/registration screen):\n> ")
            if email.lower().strip() == 'escape':
                return 'terminated'
            valid_email = is_valid_email(email)#checks that the entered email is valid and meets the required conditions
            
            # confirmation of valid email entered
            # checks if the email already exists in the database, if it doesn't it says the email is valid, if so I says the email already exists in the records
            if valid_email:
                
        
                if account_exists(email):
                    valid_email = False
                    print("The email you have entered already exists in our records, please try again.")
                else:
                    print("\nEmail is valid\n")
        
            else:
                print("Your email does not meet the requirements, please try again.")

        
        # TODO: make a helper function that ensures the password is not empty (can be similar logic to the email and name checkers, just needs to be at least one character long since we were not given any specifications on the password)
        password = getpass.getpass("Please enter the password you would like to use:\n> ")
        valid_pass = False
        if password.strip() == '':
            print("Invalid password entered")
            return 'terminated'
                
        if password.lower().strip() == 'escape':
            return 'terminated'
       
        
        name = None
        valid_name = False
        # create a helper function that ensures input has at least one non-null character
        while not valid_name: 
            name = input("\nPlease enter a valid name that you would like to go by.\nA valid name must include at least one character (not a space), have no spaces, and be less than 255 characters long.\n> ")
            if name.lower().strip() == 'escape':
                return 'terminated'
            valid_name = is_valid_name(name)#if the name is valid, this will evaluate to true and the loop will terminate
            
            # testing purposes
            # print(f"'{name}'")
            if not valid_name:
                print("Your name does not meet the requirements, please try again")
            else:
                print("Name is valid")
        #TODO: prompt for and validate:

        # birth year(ask if they want to include, make sure it is earlier than the current year)

        valid_byear = False

        while not valid_byear:
            byear = None
            byear = input("\nPlease enter a valid birth year in the form XXXX, between 1900 and 2024 (Enter 'escape' if you would like to cancel registration)\n")
            if byear.lower().strip() == 'escape':
                return 'terminated'
            elif not byear.isdigit() or int(byear) > 2024 or int(byear) < 1900:
                print("Invalid birth year, try again")
            elif len(byear) == 4 and int(byear) <= 2024 and int(byear) >= 1900:
                valid_byear = True
                byear = int(byear)

        # faculty (ask if they want to include, make sure it meets the constraints)

        valid_faculty = False
        faculty = None
        
        while not valid_faculty:
            
            faculty = input("\nPlease enter your faculty name (Enter 'escape' if you would like to cancel registration)\n")
            
            if faculty.lower() == 'escape':
                return 'terminated'
            valid_faculty = is_valid_faculty(faculty)
            
            # testing purposes
            # print(f"'{faculty}'")
            if not valid_faculty:
                 print("Your faculty name does not meet the requirements, please try again")
            else:
                print("Faculty name is valid")
                
            
            
        # insert the tuple with all of the given information once it gets validated
                   
        #insert_data()
        signed_up = True #for testing this is reached whenever all of the previous checks are successful, this is considered a successful signup, need to implement checks for the rest of the fields, then insert data once that data is validated
        
        if insert_values("members", f"('{email}', '{password}', '{name}', {int(byear)}, '{faculty}')"):
            print("\nUser Successfully Registered!!\n")
        else:
            print("\nCould not add user info to database\n")

        #return 'success'
        
    return email



def get_user_action():
# displays a menu of options for the user to select from

# must: validate entry, pass the entry to main in order to process the user selection, continue prompting user until a valid selection is made

# if user selects to logout, should be sent back to the login or register prompt screens

    #stores a list of the user's valid choices
    valid_choices = (['1','2','3','4','5'])
    user_choice = None
    #takes user input as a choice of what to do
    while user_choice not in valid_choices: 
        user_choice = (input("Please enter an option from the following menu:\n\n1.) Open Profile\n2.) Return a Book\n3.) Search for a Book\n4.) Pay a Penalty\n5.) Logout\n(or enter 'quit' to exit the application entirely)\n\n> "))
    
    #checks that the user's choice is in the list of valid options, continues prompting for an option until a valid choice is given
        if user_choice in valid_choices and user_choice != 'quit':
            return user_choice
        elif user_choice == 'quit':
            print("\nSee you next time :)")
            connection.close()
            sys.exit(0)
        else:
            print(f"\n'{user_choice}' is not a valid option.")

def login_or_signup():
    registered_user = ''
    logged_in = False #serves as a flag for the login/signup prompt loop
    while not logged_in:    
        registered_user = input("Do you currently have a registered profile? (enter 'y' or 'yes' for yes, enter 'n' or 'no' to register, or enter 'q' or 'quit' to quit): ")
            
        #condition for if the user is already registered in the databas
        #if user declares they have an account, they will move to the login page
        if registered_user.lower().strip() == 'y' or registered_user.lower().strip() == 'yes':
            #checks if the login attempt was successful
            login_attempt = attempt_login()   
            if login_attempt == 'terminated':
                
                #gets printed if the user types 'escape' while logging in 
                print("\nReturning to login/registration screen\n")#gets printed if the user types 'escape' while logging in 
            
            #if the user attempts to login but it does not succeed    
            elif not login_attempt:
                print("Login unsuccessful, username or password does not match our records. Please try again with valid credentials, signup, or enter 'q' or 'quit' to exit.")#happens if the user makes an invalid login attempt
                
            #means the login attempt was successful
            else:
                logged_in = True#login status becomes true if login is successful
                print(f"Login successful")
                email = login_attempt
                return email
                
                
        #has the same logic as the block above, but for the sign up page 
        elif registered_user.lower().strip() == 'n' or registered_user.lower().strip() == 'no':
            
            sign_up_attempt = attempt_signup()
            
                
            if sign_up_attempt == 'terminated':
                print("\nReturning to login/registration screen\n")
                
            elif not sign_up_attempt:
                print("\nSignup unsuccessful, username or password does not match our records. Please try again or type 'q' to exit.")
                #print(f"User Info: {sign_up_attempt}")#testing purposes, may be deleted later          
            else:
                logged_in = True
                email = sign_up_attempt
                return email
              
        elif registered_user.lower().strip() == 'q' or  registered_user.lower().strip() == 'quit':
            print("See you next time :)")
            connection.close()
            sys.exit(1)
        else:
            print("\nInvalid Input. Please enter 'y' for yes, 'n' for no, or 'q' to exit the application.")


def penalty_list(email):
    global cursor
    cursor.execute('drop view if exists penalty_list_view;')
    cursor.execute('create view penalty_list_view(pid,email,amount,paid_amount) as select penalties.pid, members.email, penalties.amount, ifnull(penalties.paid_amount,0) from members, penalties,borrowings where members.email = borrowings.member and borrowings.bid = penalties.bid and (penalties.amount > penalties.paid_amount or penalties.paid_amount is null);')
    cursor.execute('select * from penalty_list_view where penalty_list_view.email = ?;',(email,))
    the_list = cursor.fetchall()
    if len(the_list) == 0:
    
        print("\nYou currently have no unpaid penalties.")

        return False
    else:
       
        pid_length = len("pid")
        email_length = len("email")
        amount_length = len("amount")
        amount_paid_length = len("amount_paid")

        for y in range(len(the_list)):
            for x in range(4):
                if x == 0:
                    if len(str(the_list[y][x])) > pid_length:
                        pid_length = len(the_list[y][x])
                elif x == 1:
                    if len(the_list[y][x]) > email_length:
                        email_length = len(the_list[y][x])
                elif x == 2:
                    if len(str(the_list[y][x])) > amount_length:
                        amount_length = len(the_list[y][x])
                elif x == 3:
                    if len(str(the_list[y][x])) > amount_paid_length:
                        amount_paid_length = len(the_list[y][x])
        print('pid'.ljust(pid_length,' '),end='|')

        print('email'.center(email_length,' '),end='|')

        print('amount'.ljust(amount_length,' '),end='|')
        print('amount_paid'.ljust(amount_paid_length,' '),end='|\n')
        print("-"*(pid_length+email_length+amount_length+amount_paid_length+4))
        for y in range(len(the_list)):
            for x in range(4):
                if x == 0:
                    print(str(the_list[y][x]).ljust(pid_length,' '),end='|')
                elif x == 1:
                    print(the_list[y][x].ljust(email_length,' '),end='|')
                elif x == 2:
                    print(str(the_list[y][x]).ljust(amount_length,' '),end='|')
                elif x == 3:
                    print(str(the_list[y][x]).ljust(amount_paid_length,' '),end='|\n')
        print("\n")
            



        return True
    
                              
def user_penalty_payment(email):
    global cursor

    valid_answer = False
    while not valid_answer:
        # add no to if user wants to pay penalty
        user_input = input("Do you want to pay a penalty?\nPress 'q' or 'quit' to exit the program, 'escape' to log out, 'yes' or 'y' to pay a penalty, or 'no' or 'n' to get back to the main menu.\n> ")
        if user_input.lower() == "q" or user_input.lower() == 'quit':
            valid_answer = True
            print("\nSee you next time :)")
            sys.exit(1)
        elif user_input.lower() == "escape":
            valid_answer = True
            return "escape" # logout
        elif user_input.lower() == "n" or user_input.lower() == 'no':
            return 'no' # back to main menu
        elif user_input.lower() == "y" or user_input.lower() == "yes":
            valid_answer = True
            finished = False
            while not finished:
                cursor.execute('drop view if exists penalty_list_view;')
                cursor.execute('create view penalty_list_view(pid,email,amount,paid_amount) as select penalties.pid, members.email, penalties.amount, ifnull(penalties.paid_amount,0) from members, penalties,borrowings where members.email = borrowings.member and borrowings.bid = penalties.bid and (penalties.amount > penalties.paid_amount or penalties.paid_amount is null);')
                cursor.execute('select * from penalty_list_view where penalty_list_view.email = ?;',(email,))
                the_list = cursor.fetchall()
                
                if len(the_list) == 0:
                    return 'empty'
                else:
                   
                    pid_length = len("pid")
                    email_length = len("email")
                    amount_length = len("amount")
                    amount_paid_length = len("amount_paid")

                    for y in range(len(the_list)):
                        for x in range(4):
                            if x == 0:
                                if len(str(the_list[y][x])) > pid_length:
                                    pid_length = len(the_list[y][x])
                            elif x == 1:
                                if len(the_list[y][x]) > email_length:
                                    email_length = len(the_list[y][x])
                            elif x == 2:
                                if len(str(the_list[y][x])) > amount_length:
                                    amount_length = len(the_list[y][x])
                            elif x == 3:
                                if len(str(the_list[y][x])) > amount_paid_length:
                                    amount_paid_length = len(str(float("{:.2f}".format(float(the_list[y][x])))))# 1 edit
                    print('pid'.ljust(pid_length,' '),end='|')
                    
                    print('email'.center(email_length,' '),end='|')

                    print('amount'.ljust(amount_length,' '),end='|')
                    print('amount_paid'.ljust(amount_paid_length,' '),end='|\n')
                    print("-"*(pid_length+email_length+amount_length+amount_paid_length+4))
                    for y in range(len(the_list)):
                        for x in range(4):
                            if x == 0:
                                print(str(the_list[y][x]).ljust(pid_length,' '),end='|')
                            elif x == 1:
                                print(the_list[y][x].ljust(email_length,' '),end='|')
                            elif x == 2:
                                print(str(the_list[y][x]).ljust(amount_length,' '),end='|')
                            elif x == 3:
                                print(str(the_list[y][x]).ljust(amount_paid_length,' '),end='|\n')
            



                pid = input("Please type the pid of the penalty that you wish to pay or '-1' to cancel the transaction and return to main menu.\n>")
                status = False
                try:
                    pid = int(pid)
                    for y in range(len(the_list)):
                        for i in range(4):
                                if pid == the_list[y][i]:
                                        status = True
                                        break
                        if status == True:
                                break
                except:
                    pass
                if pid == -1:
                    finished = True
                    return 'no'
                elif type(pid) == int and status == True:
                    valid_amount = False
                    while not valid_amount:
                    
                        amount = input("Please type the amount that you would like to pay.\n> ")
                        
                        try:
                            amount = float("{:.2f}".format(float(amount))) #2 edits
                        except:
                            print("\n***Invalid input***\n")
                        
                        if type(amount) == float and amount >= 0: #3 edits
                            valid_amount = True
                        # else:
                        #     print("\n***Invalid input***\n")
                    cursor.execute('update penalties set paid_amount = ifnull(paid_amount,0) + ? where pid = ?;',(amount,pid,))

                else:
                    print("\n***Invalid input***\n")
                
        else:
            print("\n***Invalid input***\n")
            # print("Do you want to pay a penalty?\nPress 'q' or 'quit' to exit the program, 'escape' to log out, 'yes' or 'y' to pay a penalty.")
    return None


# handles user decisions once they've logged out of the system
def choose_signout_option()-> bool:
    decision_made = False
    while not decision_made:
        #The user is prompted to choose what their next action will be once they've logged out
        sign_in_or_exit = input("Would you like to return to the login screen? (enter 'y' or 'yes' if yes or enter 'quit' or 'no' to exit the program entirely)\n> ")
        # User chooses to login again
        if sign_in_or_exit.lower().strip() == 'y' or sign_in_or_exit.lower().strip() == 'yes':
            decision_made = True
            print("\nReturning to Login/Registration Screen.\n")
        # User chooses to exit the program   
        elif sign_in_or_exit.lower().strip() == 'quit' or sign_in_or_exit.lower().strip() == 'no':
            print("See you next time :)")
            sys.exit(3)
        # User makes an invalid entry
        else:
            print(f"\n'{sign_in_or_exit}' is not a valid choice.\nPlease make a valid choice.\n")  
    return decision_made

def get_members(email):

    # Retrieve personal information
    cursor.execute("SELECT name, email, byear FROM members WHERE email = ?", (email,))
    personal_info = cursor.fetchone()

    # Retrieve borrowing information
    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NOT NULL", (email,))
    previous_borrowings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL", (email,))
    current_borrowings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL AND DATE(start_date, '+20 days') < DATE('now')", (str(email),))
    overdue_borrowings = cursor.fetchone()[0]

    # Retrieve penalty information
    cursor.execute("SELECT COUNT(*) FROM penalties WHERE bid IN (SELECT bid FROM borrowings WHERE member = ?) AND paid_amount < amount", (email,))
    unpaid_penalties = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount - paid_amount) FROM penalties WHERE bid IN (SELECT bid FROM borrowings WHERE member = ?) AND paid_amount < amount", (email,))
    total_debt_amount = cursor.fetchone()[0]

    # Display the user's profile information
    if personal_info:
        print("\n-------------------------------------")
        print("USER PROFILE:")
        print("Name:", personal_info[0])
        print("Email:", personal_info[1])
        print("Birth Year:", personal_info[2])
        print("Previous Borrowings:", previous_borrowings)
        print("Current Borrowings:", current_borrowings)
        print("Overdue Borrowings:", overdue_borrowings)
        print("Unpaid Penalties:", unpaid_penalties)
        print("Total Debt Amount:", total_debt_amount)
        print("----------------------------------------\n")
    else:
        print("User not found.")


def return_book_table_stats(email):
    ''' First the system should display the user's current borrowings, as a list of the 

    borrowing id, book title, borrowing date, and return deadline for each unreturned 
    borrowing (including overdue ones). The return deadline is 20 days after the borrowing 
    date. User can pick a borrowing to return, and the system should record today’s date as 
    the returning date.
    
    The system must apply a penalty of $1 per every 
    delayed day after the deadline. For example, if a 
    book is returned after 25 days, the user will get a 
    penalty of $5 for this borrowing.'''
    # shows books that have been returned
  
    cursor.execute("SELECT b.bid, books.title, b.start_date, DATE(b.start_date, '20 days') AS return_deadline FROM borrowings b JOIN books ON b.book_id = books.book_id WHERE b.member = ? and b.end_date IS NULL;",(email,))
    borrowings = cursor.fetchall()
    #See you
    if borrowings:
        print("Current borrowings\n")
        print(f"{'Borrowing id': ^15}", " | " ,f"{'Book Title' : ^15}", " | ", f"{'Borrowing Date': ^15}", " | ", f"{'Return Deadline' : ^15}")

        for book in borrowings:
            print("{:^16} | {:^17} | {:^17} | {:^17}".format(*book))
        
        offer_to_return_book(email)

    else:
        print("You have no borrowings")

    # GOAL OF THIS FUNCTION IS SIMPLY TO DISPLAY THE TABLE AND INFORMATION

def offer_to_return_book(email):
    loop = True
    while loop:
        bid = input("Enter the borrowing ID you want to return (Enter 'escape' if you would not like to return a book): ")

        if bid.lower() == 'escape':
            break

        cursor.execute("SELECT 1 FROM borrowings WHERE bid = ? AND member = ? AND end_date IS NULL", (bid, email))
        result = cursor.fetchone()

        if result:
            cursor.execute("UPDATE borrowings SET end_date = DATE('now') WHERE bid = ?", (bid,))
            connection.commit()
            print("Book returned successfully")

            # cursor.execute("DELETE FROM borrowings WHERE bid = ?", (bid,))


            # Get the data to calculate if penalty applies
            cursor.execute("SELECT end_date, DATE(start_date, '+20 days') FROM borrowings WHERE bid = ?", (bid,))
            return_date, return_deadline = cursor.fetchone()

            # calc num of days
            new_return_date = datetime.strptime(return_date,'%Y-%m-%d')
            new_return_deadline = datetime.strptime(return_deadline,'%Y-%m-%d')
            delay_days = (new_return_date - new_return_deadline).days
            
            # delay_days = (return_deadline - return_date).days
            # print(f'\n{delay_days}\n')
            # if over 20 days
            if delay_days > 0:
                penalty_amount = delay_days  # $1 per delayed day
                print(f"You returned the book {delay_days} days after the deadline. You have recieved a penalty of ${penalty_amount}.")

                # Do we just increment the pid?

                cursor.execute("SELECT MAX(pid) FROM penalties")
                max_pid = cursor.fetchone()[0]
                if max_pid:
                    max_pid = max_pid + 1
                else:
                    max_pid = 1

                cursor.execute("INSERT INTO penalties (pid, bid, amount, paid_amount) VALUES (?, ?, ?, ?)", (max_pid, bid, penalty_amount, 0))
                print(f"Your penalty ID is {max_pid}")


         
            offer_to_write_review(email,bid)
            loop = False
        else:
            print("You have no current borrowings with the specified borrowing ID.")


def offer_to_write_review(email,borrowings_id):
    cursor.execute('select book_id from borrowings where bid = ?;',(borrowings_id,))
    book_id = cursor.fetchone()[0]
    print("Would you like to review the book you just returned?\n")
    review_choice = input("Press 'y' to review the book you have just returned, 'n' to refuse.\n> ")
    if review_choice.lower() == 'y':
        review_txt_validated = False
        while not review_txt_validated:
            review_txt = input("Please type your review for the book that you just returned.\n> ")
            if type(review_txt) == str and len(review_txt) <= 255:
                review_txt_validated = True
            else:
                print("\n***Invalid input***\n")
                print("Please type a review of less than 256 characters.\n")
        rate_num_validated = False
        while not rate_num_validated:
            rate_num = input("Please rate the book between 1 to 5 (inclusive).\n> ")
            try:
                rate_num = int(rate_num)
                if rate_num <= 5 and rate_num >= 1:
                    rate_num_validated = True
            except:
                print("\n***Invalid input***\n")
        cursor.execute('select * from reviews')
        highest_rid = cursor.fetchall()[-1][0] + 1
        the_date = str(date.today())
        
        cursor.execute('insert into reviews(rid, book_id, member, rating, rtext, rdate) values (?,?,?,?,?,DATE("now"));',(highest_rid,book_id,email,rate_num,review_txt,))
        print("Thank you.")
        connection.commit()
        #########TESTING
        # cursor.execute('select * from reviews')
        # test = cursor.fetchall() 
        # print(f'\n{test[-1]}\n')


    elif review_choice.lower() == 'n':
        return
    else:
        print("\n***Invalid input***\n")

def search_book(word):
    ''' 
    Find names of user that matches with keyword and is stored in name_matches 
    Arguments:
        word(string): name of a user
    Return: 
        name_matches(int): number of users with like names 
    '''
    global connection, cursor
    print('\n---------------Books---------------')
    cursor.execute("""
    SELECT book_id, title, author, pyear, AVG_rating AS rating, Availability
    FROM (
        SELECT b.book_id, b.title, b.author, b.pyear, IFNULL(AVG(rating), 'NA') AS AVG_rating,
               CASE
                   WHEN EXISTS (SELECT 1 FROM borrowings WHERE book_id = b.book_id AND end_date IS NULL) THEN 'Not Available'
                   ELSE 'Available'
               END AS Availability,
               CASE
                   WHEN b.title LIKE ? THEN 0
                   ELSE 1
               END AS match_order
        FROM books b 
        LEFT JOIN reviews ON reviews.book_id = b.book_id AND reviews.rating IS NOT NULL  
        WHERE b.title LIKE ? OR b.author LIKE ? 
        GROUP BY b.book_id, b.title, b.author, b.pyear
    ) AS CombinedResults
    ORDER BY match_order, 
         CASE WHEN match_order = 0 THEN title END, 
         CASE WHEN match_order = 0 THEN LENGTH(title) END, 
         CASE WHEN match_order = 0 THEN LENGTH(author) END
""", ('%' + word + '%', '%' + word + '%', '%' + word + '%'))


    book_matches = cursor.fetchall()
   
    book_count = len(book_matches)
  
   
   # this loop checks if a valid search is entered if no elements are shown then it is isn't a valid search so we reprompt the user if they want to search again
    while(True):
        if (book_count == 0):
            keyword_not_found = input("No result found for search would you like to try again y/n ")
            try:
                if(keyword_not_found == 'n'):
                    print("Chose not to search again. Search exited. Return to Main Menu")
                    return -1
                if(keyword_not_found == 'y'):
                    return 2
                else:
                     raise ValueError("Must enter either n or y")
            except ValueError as e:
                print("Error:", e)
        else:
            break
    #max num of element displayed each time is 5 //description
    match_titles = []
    max_print = 5
    i = 0        
    while( i < book_count):
        if(i < book_count and i<max_print):
            match_titles.append(book_matches[i])
            print(*book_matches[i])
            i+=1
        
        if (i == max_print and i<book_count):
            fivemore = input("Show More, Continue to Next Page? y/n: ")
            if fivemore == 'y':
                max_print += 5
            elif fivemore == 'n':
                break
            else:
                print("must enter either y or n")
        
    return match_titles

def borrow_book(b_code,email):
    global connection, cursor
    # Check if the book is already borrowed
    cursor.execute("SELECT * FROM borrowings br, books b WHERE br.book_id = ? AND br.end_date IS NULL", (b_code,))
    already_borrowed = cursor.fetchone()

    if already_borrowed:
        return 2
    else:
        # Book is not borrowed, so insert a new row into borrowings table
        # Generate a unique bid (borrow ID) and set today's date as the start date
        cursor.execute("SELECT MAX(bid) FROM borrowings")
        max_bid = cursor.fetchone()[0]
        if max_bid:
            max_bid = max_bid + 1 
        else:
            max_bid = 1
       
        s_date = datetime.now()
        start_date = str(s_date.date())
    
    cursor.execute("INSERT INTO borrowings (bid, member, book_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)", (max_bid, email ,b_code, start_date, None))
    connection.commit()
    print("Book borrowed successfully!")
    return
   
def getBook(b_identity):
    books = []
    for book in b_identity:
        books.append(book[0])
    return books 

def display(email):
    while True:
        user_choice = get_user_action()
        # make if else conditions for all of the possible functionalities in the program   

        if user_choice == '1':
            get_members(email)
        


        elif user_choice == '2':

            # first that program shows a table of all of the books that need to be returned
            # if there are not such books then the program informs that user of that
            return_book_table_stats(email)
            # returning = True
            
                    
        elif user_choice == '3':
            keyword = input("Search For a Book: ")
            output = search_book(keyword)
            while True:
                if output == -1:
                    break
            
                if output == 2:
                    keyword = input("Search For a Book: ")
                    output = search_book(keyword)
                    if(output != 2):
                        break
                else:
                    break

            if((output != 2) and (output != -1 )):
                chosen_book = input("Select ID of Book to Borrow or Enter n to Return to Main Menu: ")
                if (chosen_book.lower() == 'n'):
                    print("Getting back to main menu.")
                   
                stop_if = False
                if (chosen_book.lower() != 'n'):
                    book_ids = [str(book_id) for book_id in getBook(output)]
                    while (chosen_book not in book_ids):
                       
                        chosen_book = input("\nType Book ID Correctly or Type 'esc' to Return to Main Menu: ")
                        if (chosen_book.lower() == 'esc'):
                            stop_if = True
                            break
                    
                    if not stop_if:          
                        result = borrow_book(chosen_book,email)
                        if (result == 2):
                            print("Sorry, this book is not available for borrowing.")

        
                            
        elif user_choice == '4': #Pay a penalty
            current_user = email
            status_of_penalty = penalty_list(current_user)
            penalty_loop = True
            if status_of_penalty == False:
                print("Returning to main menu since there are no penalties to be paid.\n")
                penalty_loop = False

            while penalty_loop:
                answer = user_penalty_payment(current_user)
                if answer == 'escape':
                    # current_user = None
                    penalty_loop = False
                    return
                elif answer == 'no':
                    penalty_loop = False
                elif 'empty':
                    print("\nCongratulations!!!\nNo more penalties to pay.\n")
                    print("Returning to main menu since there are no penalties to be paid.\n")
                    penalty_loop = False

        elif user_choice == '5':
            current_user = None
            decision_made = False
            while not decision_made:  
                #Handles next decision after signing out from the application
                decision_made = choose_signout_option() #only returns true if the user decides to log back in, else it exits the application
            return

        else:
            print("Please Enter a Valid option")
            display(email)




###############################################################################################################################
