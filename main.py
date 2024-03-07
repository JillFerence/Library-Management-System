import sys


def Login():
    userInput = input("Do you have an account? (Y/N)")
        
    if userInput == "Y":
        print("**** Login ****")
        username = input("Enter Email: ")
        password = input("Enter Password: ")
    elif userInput == "N":
        passFlag = False 
        print("**** Register ****")
        username = input("Enter new Email: ")
        name = input("Enter your Name: ")
        birthYear = input("Enter your Year of Birth: ")
        faculty = input("Enter your Faculty: ")
        while(1):
            password = input("Enter new Password: ")
            passwordCheck = input("Re-enter password: ")
            if password != passwordCheck:
                print("Passwords do not match!")
            else:
                break
    else:
        print("Invalid Input")

def MainMenu():
    while(1):
        option = input("Choose your option (Enter Corresponding Number):\n1.Profile\n2.Your Books\n3.Book Search\n4.Pay Penalty\n5.Quit\n")
        if option == "1":
            print("Profile")
        elif option == "2":
            print("Your Books")
        elif option == "3":
            print("Book Search")
        elif option == "4":
            print("Pay Penalty")
        elif option == "5":
            break
        else:
            print("Invalid Input")

try:
    database = sys.argv[1]
except IndexError:
    print("Improper code usage, please use: \npython3 main.py \"database\"")
    sys.exit(1)
Login()
MainMenu()  