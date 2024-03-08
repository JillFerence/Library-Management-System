import sys
import sqlite3
import getpass as gp


def Login():
    while(1):
        userInput = input("\n**** Login Page ****\nDo you have an account? (Y|N):")
        
        if userInput == "Y":
            print("**** Login ****")
            while(1):
                email = input("Enter Email: ")
                password = gp.getpass("Enter Password: ")
                c.execute("SELECT email, name FROM members WHERE email=:email AND passwd=:passwd", {
                    "email": email, "passwd": password
                })
                res = c.fetchone()
                try:
                    if res[0] == email:
                        print("Successfully logged in!\nWelcome " + res[1] + "")
                        return email
                    else:
                        print("Incorrect User Information")
                except TypeError:
                    print("User not found, try again\n")
                        

                
            
        elif userInput == "N":
            passFlag = False 
            print("**** Register ****")
            email = input("Fill information below\nEmail: ")
            name = input("Name: ")
            birthYear = input("Year of Birth: ")
            faculty = input("Faculty: ")
            while(1):
                password = gp.getpass("Enter new Password: ")
                passwordCheck = gp.getpass("Re-enter password: ")
                if password != passwordCheck:
                    print("Passwords do not match!")
                else:
                    break
            try:
                c.execute("INSERT INTO members VALUES ('"+email+"','"+password+"','"+name+"',"+birthYear+",'"+faculty+"')")
                conn.commit()
                print("Account registered")
                return email
            except sqlite3.IntegrityError:
                print("This account is already registered!")
                continue
            
        else:
            print("Invalid Input (Y|N)")

def profile():
    option = input("\n\n**** Profile ****\n1.User Information\n2.Borrowed Books\n3.Penalties\n4.Logout\n")
    if option == "1":
        c.execute("SELECT email, name, byear, faculty FROM members WHERE email=:email", {
            "email": u_email,
        })
        res = c.fetchone()
        print("\n\n**** User Information ****:\nEmail: "+res[0]+"\nName: "+res[1]+"\nYear of Birth: "+str(res[2])+"\nFaculty: "+res[3])
        input("Press enter to return to main menu")
    elif option == "2":
        print("Borrowed Books") 
    elif option == "3":
        print("Penalties")
    elif option == "4":
        u_email = Login()
    

def MainMenu():
    while(1):
        option = input("\n\n**** Main Menu ****\n1.Profile\n2.Your Books\n3.Book Search\n4.Pay Penalty\n5.Quit\n(Enter corresponding number):")
        if option == "1":
            profile()
        elif option == "2":
            print("Book Return")
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