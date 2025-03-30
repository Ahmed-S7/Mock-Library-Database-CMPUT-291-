[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/50dc0VUx)
# CMPUT 291 Mini Project 1 - Winter 2024  
Group member names and ccids (3-4 members)  
  asshittu, Ahmed Shittu 
  ejiang1, Eric Jiang  
  mcherkas, Maxim Cherkasov  
  aamare, Abdi Mare

# Group work break-down strategy
Ahmed: responsible for all login/signup functionalities, adding new users, user navigation in sign-in and sign-out logic
Maxim: responsible for the system functionalities #4: Penalty, the review part of returned book.
Abdi: responsible for #3 searching/borrowing a book
Eric: responsible for viewing user profile and return book
All: general checks and bug fixes all around, testing and updating code 

# Code execution guide 
To run the code, use <python> <script.py> <./database.db> where python is your python edition (code was made with python 3.11), script.py is our code, and database.db is the database being used, running it would look like (for example): "python3.11 backup3.py ./project1.db"

Once run, the user will be prompted to either sign up or login. The user will be given to exit the program entirely by entering 'q' or 'quit' during their registration. When the user chooses to sign up (by entering 'n' or 'no'), they are asked to enter a valid email, name, faculty, and birth year. At each step, if the user enters data which does not meet the constraints, they are informed of what the issue is with their entry, and are prompted continually to enter valid inputs for these fields until they provide a valid response. The user is also given the option to return to the login/registration screen by entering 'escape' at any point during their registration. When the user chooses to login (by entering 'y' or 'yes'), they are asked to provide an email, if the email does not match the user will be prompted again. When it matches a password will be requested, the user will not be able to see the password they typed and if it is wrong they will be asked to try again. During a login, the user has the option to exit to the login/signup screen by entering 'escape'. Upon successful login, the user can do 1 of 5 things. 

1) They can view their profile, return a book/view borrowings, search for a book, pay a penalty, or logout. By typing the number '1'. They can view their profile where they can see, name, email, birth year, previous borrowings, current borrowings, overdue borrowings, unpaid penalties, and total debt amount. From there they exit back to the menu where they havae all 5 options again.

2) They can choose to return a book by typing the number '2'. Where then it will pull up a table that has any book they have borrowed alongside the title, borrowing id, start date of borrowing, and the due date of the borrowing. If they don't have any books borrowed it will tell them they have no borrowings and return them to the menu. If they do have borrowings, they are given the choice to return a book or not. If they choose to return a book by entering y when prompted, they will have to enter the borrowing ID of the book they want to return. The total penalty for that one book will be calculated and displayed when they return the book. Afterwards, they are given a y/n choice to write a review. If they type 'y', they can enter a few words for the review and then a number from 1-5 as a rating. Then they will be returned to the main menu. They will also be returned to the main menu when they type 'n'.

3) They can choose to search for a book by typing the number '3'. Then they will be prompted to search for a book, if they search something that does not exist (book with a different name) they will be prompted to type a correct name or go back into the main menu. if they search something with a matching key word then, the it will return all books where the title matches that key word or author matches that key word but in a order of titles in ascending length first then authors in ascending length. The user will then have the option to select an id of a book they search with hopes of borrowing that book, if the book is avaliable and they enter that book id then the book should print a succesful borrow message, if the book is not avaliable (someone else is borrowing the book) then a message saying the book is not avaliable for borrowing should be printed. If the user searches for a book and does not want to select a book to borrow and wants to return to main menu they can enter 'n'. If the user enters an incorrect user id then was not supported by the search they will be reprompted to enter the correct id or return to main menu by pressing 'esc' If they enter anything other than wants supported they they will be reprompted.

4) When a user types in the number '4'. They will be taken to the page where they can pay any penalties they have. If they have no penalties they will get a message telling them they have no penalties to pay and will be returned to the main menu. If they do have penalties they will be taken to a page they will be given a few options. From there they can choose to either pay, log out, exit the program, or return to menu by using 'y'/'yes | 'escape' | 'q'/'quit' | 'n/no' respectively. When they choose to pay, they will then be taken to a page that displays all their penalties. There they can see the penalty ID, email, amount owed, amount paid. They can then choose to either type the penalty ID that they would like to make a payment for or type '-1' to cancel transaction and return to main menu. Otherwise after they type the penalty ID, they can choose the amount they want to pay. The input was to be larger than 0. Afterwards they will be taken back to the same menu that they saw with all their penalties and payments where the user will have the same choices again.
   
5) When a user types in the number '5', they are logged out given an option to return to the login screen (entering 'y' or 'yes'), or to exit the program entirely (entering 'quit' or 'no').
