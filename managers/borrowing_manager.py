from datetime import datetime, timedelta

def julian_to_date(julian_day):
    unix_timestamp = (julian_day - 2440587.5) * 86400
    date = datetime.utcfromtimestamp(unix_timestamp).date()
    return date
class BorrowingManager:
    def __init__(self, db_handler, penalty_manager):
        self.db = db_handler
        self.penalty_manager = penalty_manager

    def show_borrowed_books(self, email):
        query = """
        SELECT b.bid, bk.title, b.start_date, (julianday(b.start_date) + 20) as due_date
        FROM borrowings b
        JOIN books bk ON b.book_id = bk.book_id
        WHERE b.member = ? AND b.end_date IS NULL"""

        borrowings = self.db.fetch_all(query, (email,))

        if borrowings:
            print("**** Borrowed Books ****")
            print("Borrow ID | Title | Borrowed on | Due Date | Status")
            for b in borrowings:
                # If the book is overdue, let's show that to the user
                due_date = julian_to_date(b[3])
                today = datetime.now().date()

                overdue_status = "Overdue" if due_date < today else f"Days left: {(due_date - today).days}"

                print(f"{b[0]} | {b[1]} | {b[2]} | {due_date} | {overdue_status}")


    def return_book(self, email, bid):
        borrowing_query = """
        SELECT start_date, book_id FROM borrowings WHERE bid = ? AND member = ?"""
        borrowing = self.db.fetch_one(borrowing_query, (bid, email))

        if not borrowing:
            print("Invalid Borrow ID")
            return

        start_date, book_id = borrowing

        penalty = self.penalty_manager.calculate_penalty(start_date)

        self.db.execute_query("UPDATE borrowings SET end_date = date('now') WHERE bid = ?", (bid,))

        if penalty > 0:
            self.db.execute_query("INSERT INTO penalties (bid, amount, paid_amount) VALUES (?, ?, NULL)", (bid, penalty))

        self.ask_for_review(book_id, email)

    def ask_for_review(self, book_id, email):
        user_response = input("Would you like to leave a review for the book? (y/n): ")
        if user_response.lower() == "y":
            rating = input("Enter a rating (1-5): ")
            review = input("Enter a review (or leave this blank): ")

            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating out of range")
            except ValueError as e:
                print(f"Invalid rating: {e}")
                return
            
            insertion_query = """
            INSERT INTO reviews (book_id, member, rating, rtext, rdate)
            VALUES (?, ?, ?, ?, date('now'))
            """

            self.db.execute_query(insertion_query, (book_id, email, rating, review))
            print("Review added successfully. Thanks for your feedback!")

        else:
            print("No problem, maybe next time!")

    def borrow_book(self, email, bid):
        pass #TODO implement this