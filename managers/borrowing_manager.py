from datetime import datetime, timedelta

class BorrowingManager:
    def __init__(self, db_handler):
        self.db = db_handler

    def show_borrowed_books(self, email):
        pass #TODO implement this

    def return_book(self, email, bid):
        pass #TODO implement this

    def borrow_book(self, email, bid):
        pass #TODO implement this