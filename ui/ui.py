import getpass as gp

class UI:
    def __init__(self, auth_system):
        self.auth = auth_system
        self.user = None

    def show_member_profile(self):  
        member_info = self.auth.db.get_member_info(self.user[0])
        print(f"\n**** Member Profile: {member_info[0]} ****\n")
        print("**** User Information ****")
        print(f"Email: {member_info[1]}\nBirth Year: {member_info[2]}\n")

        borrowing_info = self.auth.db.get_borrowing_info(self.user[0])
        print("**** Borrowing Information ****")
        print(f"Total Books Borrowed: {borrowing_info[0]}\nCurrent Books Borrowed: {borrowing_info[1]}\nOverdue Books Borrowed: {borrowing_info[2]}\n")

        penalty_info = self.auth.db.get_penalty_info(self.user[0])
        print("**** Penalty Information ****")
        print(f"Unpaid Penalties: {penalty_info[0]}\nTotal Penalty Debt: {penalty_info[1]}\n")

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
                pass #TODO implement this
            elif choice == "3":
                self.show_book_search_start()
            elif choice == "4":
                self.show_penalty_menu()
            elif choice == "5":
                self.logout()
                break
            else:
                print("Invalid Input. Please try again.")

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
                if payment > amount_owed:
                    print("Payment cannot be more than owed amount")
                elif payment <= 0:
                    print("Must pay more than $0")
                elif payment == amount_owed:
                    self.auth.db.pay_penalty_in_full(pid)
                    return
                else:
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

    def login(self):
        print("\n**** Login ****")
        email = input("Email: ")
        self.user = self.auth.login(email) # This is the reason for the auth handler

        if self.user is not None:
            self.show_member_menu()
        else:
            print("Invalid email or password. Try again or sign up if you don't already have an account.")
            self.show_start_menu()
    
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

    def logout(self):
        self.user = None
        print("Logged out successfully!")
        self.show_start_menu()

    # ******************
    # BOOK SEARCH
    # ******************
    
    # Displays the book search title and prompt the user for a keyword
    def show_book_search_start(self):
        keyword = input("\n**** Book Search ****\nEnter a keyword: ")
        print("\nBooks that match the keyword " + keyword + ":\n")
        self.show_book_search_items(keyword, page = 1)
    
    # Organizes the display of books and options in the book search
    def show_book_search_items(self, keyword, page):
        limit = 5 # Book display limit
        books = self.auth.db.get_book_search_info(keyword, limit, page)
        self.show_book_search_books(books)
        # Check if there are more than the limit number of books to display
        more_books = False
        if len(books) == limit:
            more_books = True
        self.show_book_search_options(more_books, keyword, page)
    
    # Displays the books in the book search
    def show_book_search_books(self, books):
        for k in books:
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

            print("Book ID: " + book_id + " Title: " + title + " Author: " + author + " Publish Year: " + pyear + " Average Rating: " + avg_rating + " Availability: " + availability)

    def show_book_search_options(self, more_books, keyword, page):
        while(1):
            option = input("\n1. See More Books\n2. Borrow a Book\n3. Main Menu\n(Enter corresponding number): ")
            if option == "1":
                if more_books:
                    self.show_book_search_items(keyword, page = page + 1)
                else:
                    print("There are no more books with this search.")
                    self.show_book_search_options(more_books, keyword, page)
            elif option == "2":
                self.show_book_search_borrow(more_books, keyword, page)
            elif option == "3":
                self.show_member_menu()
            else:
                print("Invalid Input")

    def show_book_search_borrow(self, more_books, keyword, page):
        book_id = input("\nEnter a the book ID of the book you want to borrow: ")
        # If the book id is invalid
        validity = self.auth.db.check_book_id_validity(book_id)
        if validity == False:
            print("Invalid book ID.")
            return
        # If the book is not apart of the search list 
        in_list = self.auth.db.check_book_id_in_list(book_id)
        if in_list == False:
            print("You must select a book ID that is in the search list shown above.")
            return
        # If the book is available to borrow
        availability = self.auth.db.check_book_id_availability(book_id)
        if availability == False:
            print("This book is not available to borrow at the moment.")
        else:
            print("This book is available to borrow!")
            user_input = input("You will have 20 days to return this book after borrowing it. Are you sure you want to borrow this book? (Y|N): ")
            if user_input == 'Y':
                self.auth.db.borrow_book(self.user[0], book_id)
                print("The book was borrowed successfully, you have 20 days to return the book.")
                self.show_book_search_options(more_books, keyword, page)
            elif user_input == 'N':
                print("Process cancelled, the book was not borrowed.")
                self.show_book_search_options(more_books, keyword, page)
            else:
                print("Invalid Input (Y|N)")


       
    
