import getpass as gp
from db.db_handler import DatabaseHandler

"""
******************************
AUTHENTICATION CLASS
******************************
"""
class Auth:
    # Initialization method for the auth class
    def __init__(self, db_handler):
        self.db = db_handler
    
    # Method for the user to login
    def login(self, email):
        password = gp.getpass("Enter Password: ")

        user_query = "SELECT * FROM members WHERE email = ? AND passwd = ?"
        user = self.db.fetch_one(user_query, (email, password))

        if user:
            return user # Let's return the user object for now
        else:
            return None
        
    # Method for the user to signup
    def signup(self, email, password, name, birthYear, faculty):
        # First let's check if the user already exists
        user_query = "SELECT * FROM members WHERE email = ?"
        user = self.db.fetch_one(user_query, (email,))
        if user:
            return None
        
        # If the user does not exist, let's register the user
        insert_query = "INSERT INTO members VALUES (?, ?, ?, ?, ?)"
        self.db.execute_query(insert_query, (email, password, name, birthYear, faculty))
        print("Signup successful!")
        user = self.db.fetch_one(user_query, (email,)) # Let's fetch the user again to return

        # Not sure if we really need all this Null checking, but let's keep it for now
        if user:
            return user
        else:
            return None