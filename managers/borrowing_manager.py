from datetime import datetime, timedelta

class BorrowingManager:
    def __init__(self, db_handler):
        self.db = db_handler

    def show_borrowed_books(self, email):
        query = """
        SELECT b.bid, bk.title, b.start_date, (julianday(b.start_date) + 20) as due_date
        FROM borrowings b
        JOIN books bk ON b.book_id = bk.bid
        WHERE b.member = ? AND b.end_date IS NULL"""

        borrowings = self.db.fetch_all(query, (email,))

        if borrowings:
            print("**** Borrowed Books ****")
            for b in borrowings:
                # If the book is overdue, let's show that to the user
                overdue_status = "Overdue" if b[3] < datetime.now().date() else "Days left: " + str((b[3] - datetime.now().date()).days)
                print(f"Book ID: {b[0]}, Title: {b[1]}, Borrowed on: {b[2]}, Due Date: {b[3]}, {overdue_status}")


    def return_book(self, email, bid):
        pass #TODO implement this

    def borrow_book(self, email, bid):
        pass #TODO implement this