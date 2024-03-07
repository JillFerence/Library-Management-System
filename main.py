import sys
import sqlite3
import enum


def Login():
    while(1):
        userInput = input("Do you have an account? (Y/N):")
            
        if userInput == "Y":
            print("**** Login ****")
            while(1):
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                c.execute("SELECT email, name FROM members WHERE email=:email AND passwd=:passwd", {
                    "email": email, "passwd": password
                })
                res = c.fetchone()
                
                if res[0] == email:
                    print("Successfully logged in! Welcome " + res[1] + "")
                    return email
                else:
                    print("User account not found!")

                
            
        elif userInput == "N":
            passFlag = False 
            print("**** Register ****")
            email = input("Enter new Email: ")
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
            c.execute("INSERT INTO members VALUES ('"+email+"','"+password+"','"+name+"',"+birthYear+",'"+faculty+"')")
            conn.commit()
            return email
        else:
            print("Invalid Input")

def MainMenu():
    while(1):
        option = input("\n\nChoose your option (Enter Corresponding Number):\n1.Profile\n2.Your Books\n3.Book Search\n4.Pay Penalty\n5.Quit\n")
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
conn = sqlite3.connect(database)
c = conn.cursor()
u_email = Login()
MainMenu()