import getpass as gp

class UI:
    def __init__(self, auth_system, borrowing_manager, book_manager, penalty_manager, profile_manager):
        self.auth = auth_system
        self.borrowing_manager = borrowing_manager
        self.book_manager = book_manager
        self.penalty_manager = penalty_manager
        self.profile_manager = profile_manager
        self.user = None

    def show_member_profile(self):  # TODO make this use profile_manager.py!!!
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

    def return_a_book(self):
        print("\n**** Return a Book ****\n")

        print("My Borrowed Books: ")
        self.borrowing_manager.show_borrowed_books(self.user[0])

        bid = input("Enter Book ID: of the book you want to return: ")

        self.borrowing_manager.return_book(self.user[0], bid)
        

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
                pass #TODO implement this
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
