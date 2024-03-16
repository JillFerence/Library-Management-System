import getpass as gp

"""
******************************
USER INTERFACE CLASS
******************************
"""
class UI:
    # Initialization method for the User Interface class
    def __init__(self, auth_system, borrowing_manager, book_manager, penalty_manager, profile_manager):
        self.auth = auth_system
        self.borrowing_manager = borrowing_manager
        self.book_manager = book_manager
        self.penalty_manager = penalty_manager
        self.profile_manager = profile_manager
        self.user = None
        self.shown_book_ids = [] # List of book ids that are currently displayed

    """
    ******************************
    MEMBER PROFILE UI METHODS
    ******************************
    """
    # Displays the member profile information
    def show_member_profile(self):  # TODO make this use profile_manager.py!!!
        # Displays the user information 
        member_info = self.auth.db.get_member_info(self.user[0])
        print(f"\n**** Member Profile: {member_info[0]} ****\n")
        print("**** User Information ****")
        print(f"Email: {member_info[1]}\nBirth Year: {member_info[2]}\n")
        # Displays the borrowing information 
        borrowing_info = self.auth.db.get_borrowing_info(self.user[0])
        print("**** Borrowing Information ****")
        print(f"Total Books Borrowed: {borrowing_info[0]}\nCurrent Books Borrowed: {borrowing_info[1]}\nOverdue Books Borrowed: {borrowing_info[2]}\n")
        # Displays the penalty information 
        penalty_info = self.auth.db.get_penalty_info(self.user[0])
        print("**** Penalty Information ****")
        print(f"Unpaid Penalties: {penalty_info[0]}\nTotal Penalty Debt: {penalty_info[1]}\n")
    
    """
    ******************************
    BOOK RETURN UI METHODS
    ******************************
    """
    # Method to display the book return process
    def return_a_book(self):
        print("\n**** Return a Book ****\n")

        print("My Borrowed Books: ")
        self.borrowing_manager.show_borrowed_books(self.user[0])

        bid = input("Enter Borrow ID: of the book you want to return: ")

        self.borrowing_manager.return_book(self.user[0], bid)
    
    """
    ******************************
    MAIN MENU UI METHODS
    ******************************
    """
    # Displays the member main menu 
    def show_member_menu(self):
        while True:
            print("\n**** Member Menu ****")
            print("1. View Profile")
            print("2. Return a book")
            print("3. Search for a book")
            print("4. Pay Penalty")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                self.show_member_profile()
            elif choice == "2":
                self.return_a_book()
            elif choice == "3":
                self.show_book_search_start()
            elif choice == "4":
                self.show_penalty_menu()
            elif choice == "5":
                self.logout()
                break
            else:
                print("Invalid Input. Please try again.")

    # Displays the start main menu
    def show_start_menu(self):
        print("\n**** Welcome! ****")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice =  input("Enter choice: ")
    
        if choice == "1":
            self.login()
        elif choice == "2":
            self.signup()
        elif choice == "3":
            print("Goodbye!")
            quit()
        else:
            print("Invalid Input. Please try again.")
            self.show_start_menu()
    
    """
    ******************************
    PAY PENALTY UI METHODS
    ******************************
    """
    # Prompts user to select penalty ID as well as payment amount
    # Ensures proper data entry, as well as calls to database handler
    def process_payment(self, penatlies):
        pidFlag = True
        pid = int(input("\n\nEnter Penalty ID: "))
        payment = int(input("Enter Payment Amount: "))
        for row in penatlies:
            if row[0] == pid:
                pidFlag = False
                amount_owed = row[3] - row[4]
                if payment > amount_owed: # If user trying to pay more than the amount owed
                    print("Payment cannot be more than owed amount")
                elif payment <= 0: # If user trying to pay with an invalid amount
                    print("Must pay more than $0")
                elif payment == amount_owed: # If user payed exactly the amount owed
                    self.auth.db.pay_penalty_in_full(pid)
                    return
                else: # If user payed a portion of the amount owed
                    self.auth.db.pay_pentalty_partially(pid, payment, row[4])
                    return
        if(pidFlag):
            print("Penalty ID not found")
        cFlag = input("Do you want to retry? (y/n): ")
        if(cFlag == "y" or cFlag == "Y"):
            self.process_payment(penatlies)

    # Displays list of penalties using get_penalties in the db handler,
    # Calls process_payment so a user can interact with the penalties
    def show_penalty_menu(self):
        print("\n**** Penalties ****")
        print("Penalty ID | Title | Borrow ID | Amount Owed")
        penalties = self.auth.db.get_penalties(self.user[0])
        for row in penalties:   
            print("  %s |  %s | %s | $%d" % (row[0], row[1], row[2], row[3] - row[4]))
        self.process_payment(penalties)

    """
    ******************************
    LOGIN/SIGN UP UI METHODS
    ******************************
    """
    # Login method for the user
    def login(self):
        print("\n**** Login ****")
        email = input("Email: ")
        self.user = self.auth.login(email) # This is the reason for the auth handler

        if self.user is not None: # If the member exists
            self.show_member_menu()
        else:
            print("Invalid email or password. Try again or sign up if you don't already have an account.")
            self.show_start_menu()
    
    # Sign up method for the user
    def signup(self):
        print("\n**** Sign Up ****")
        email = input("Fill information below\nEmail: ")
        name = input("Name: ")
        birthYear = input("Year of Birth: ")
        faculty = input("Faculty: ")
        password = gp.getpass("Enter new Password: ")

        self.user = self.auth.signup(email, password, name, birthYear, faculty)

        if self.user is not None:
            self.show_member_menu()
        else:
            print("This account is already registered!")
            self.show_start_menu()

    # Logout method for the user
    def logout(self):
        self.user = None
        print("Logged out successfully!")
        self.show_start_menu()

    """
    ******************************
    BOOK SEARCH UI METHODS
    ******************************
    """
    # Displays the book search introction
    def show_book_search_start(self):
        self.shown_book_ids = []
        print("\n**** Book Search ****")
        keyword = input("Enter a keyword to begin the book search: ")
        print("Here is a list of books with titles or authors that match the keyword " + keyword + ": \n")
        self.show_book_search_items(keyword, page = 1)
    
    # Organizes the display of books and options in the book search
    def show_book_search_items(self, keyword, page):
        limit = 5 # Book display limit
        books = self.auth.db.get_book_search_info(keyword, limit, self.shown_book_ids, page)
        self.show_book_search_books(books)
        # Check if there are more than the limit number of books to display
        more_books = False
        if len(books) == limit:
            more_books = True
        self.show_book_search_options(more_books, keyword, page)
    
    # Displays the books in the book search
    def show_book_search_books(self, books):
        for k in books:
            # If any of the information is missing, default to N/A
            if k[0] == None: book_id = "N/A" 
            else: book_id = str(k[0])
            if k[1] == None: title = "N/A" 
            else: title = str(k[1])
            if k[2] == None: author = "N/A" 
            else: author = str(k[2])
            if k[3] == None: pyear = "N/A" 
            else: pyear = str(k[3])
            if k[4] == None: avg_rating = "N/A" 
            else: avg_rating = str(k[4])
            if k[5] == None: availability = "N/A" 
            else: availability = str(k[5])

            print("  Book ID: " + book_id + " Title: " + title + " Author: " + author + " Publish Year: " + pyear + " Average Rating: " + avg_rating + " Availability: " + availability)

    # Displays the book search options 
    def show_book_search_options(self, more_books, keyword, page):
        while(1):
            print("\n1. See More Books")
            print("2. Borrow a Book")
            print("3. Start a New Book Search")
            print("4. Main Menu")
            option = input("Enter choice: ")
            if option == "1":
                if more_books: # If there is more books that can be displayed that match the keyword
                    self.show_book_search_items(keyword, page = page + 1)
                else: # If there are no more books that can be displayed that match the keyword
                    print("There are no more books with this search.")
                    self.show_book_search_options(more_books, keyword, page)
            elif option == "2":
                self.show_book_search_borrow(more_books, keyword, page)
            elif option == "3":
                self.show_book_search_start()
            elif option == "4":
                self.show_member_menu()
            else:
                print("Invalid Input. Please try again.")

    # Displays the prompt when the user wants to borrow a book from the book search list
    def show_book_search_borrow(self, more_books, keyword, page):
        print("**** Borrow a Book ****")
        book_id = input("Enter a the book ID of the book you want to borrow: ")
        # If the book id is invalid
        validity = self.auth.db.check_book_id_validity(book_id)
        if validity == False:
            print("Invalid book ID, this book ID does not exist in the system.")
            return
        # If the book is not apart of the search list 
        in_list = self.auth.db.check_book_id_in_list(book_id, self.shown_book_ids)
        if in_list == False:
            print("You must select a book ID that is in the search list.")
            return
        # If the book is available to borrow
        availability = self.auth.db.check_book_id_availability(book_id)
        if availability == False:
            print("This book is not available to borrow at the moment.")
        else:
            print("This book is available to borrow!")
            while(1):
                user_input = input("You will have 20 days to return this book after borrowing it. Are you sure you want to borrow this book? (Y|N): ")
                if user_input.lower() == 'y':
                    self.auth.db.borrow_book(self.user[0], book_id)
                    print("The book was borrowed successfully, you have 20 days to return the book.")
                    self.show_book_search_options(more_books, keyword, page)
                elif user_input.lower() == 'n':
                    print("Process cancelled, the book was not borrowed.")
                    self.show_book_search_options(more_books, keyword, page)
                else:
                    print("Invalid Input. Please enter y for yes or n for no.")
