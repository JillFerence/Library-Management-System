import getpass as gp

class UI:
    def __init__(self, auth_system):
        self.auth = auth_system
        self.user = None

    def show_member_profile(self):  
        print("\n**** Member Profile ****")
        print("Name: " + self.user[2])
        print("Email: " + self.user[0])
        print("Year of Birth: " + str(self.user[3]))
        print("Faculty: " + self.user[4] + "\n")

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
                pass #TODO implement this
            elif choice == "4":
                pass #TODO implement this
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
