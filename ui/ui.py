import getpass as gp

class UI:
    def __init__(self, auth_system):
        self.auth = auth_system

    def show_start_menu(self):

        while True:
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
                break
            else:
                print("Invalid Input. Please try again.")

    def login(self):
        print("\n**** Login ****")
        email = input("Email: ")
        user = self.auth.login(email) # This is the reason for the auth handler

        if user is not None:
            print("Welcome back, " + user[2])
            #TODO Here we will navigate to the user's profile in the future
        else:
            print("Invalid email or password. Try again or sign up if you don't already have an account.")
    
    def signup(self):
        print("\n**** Sign Up ****")
        email = input("Fill information below\nEmail: ")
        name = input("Name: ")
        birthYear = input("Year of Birth: ")
        faculty = input("Faculty: ")
        password = gp.getpass("Enter new Password: ")

        successfull_login = self.auth.signup(email, password, name, birthYear, faculty)

        if successfull_login is not None:
            #TODO Here we will navigate to the user's profile in the future
            pass

    def logout(self):
        self.auth.logout()
        print("Logged out successfully!")