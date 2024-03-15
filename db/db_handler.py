import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    def execute_query(self, query, params):
        try:
            c = self.conn.cursor()
            c.execute(query, params)
            self.conn.commit()
            return c
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    def fetch_one(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchone()
        else:
            return None
    
    def fetch_all(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchall()
        else:
            return []
        
    def close_connection(self):
        status = self.conn.close()
        if status:
            print("Connection closed")
        else:
            print("Connection is already closed")
    
    def get_member_info(self, email):
        query = "SELECT name, email, byear FROM members WHERE email = ?"
        return self.fetch_one(query, (email,))
    
    def get_borrowing_info(self, email):
        
        borrow_query = "SELECT COUNT(*) FROM borrowings WHERE member = ?"
        total_borrowed = self.fetch_one(borrow_query, (email,))
        if total_borrowed is not None:
            total_borrowed = total_borrowed[0]
        else:
            total_borrowed = 0
        
        current_borrow_query = "SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL"
        current_borrowed = self.fetch_one(current_borrow_query, (email,))
        if current_borrowed is not None:
            current_borrowed = current_borrowed[0]
        else:
            current_borrowed = 0
        
        overdue_borrowings_query = """
            SELECT COUNT(*)
            FROM borrowings
            WHERE member = ? AND end_date IS NULL AND DATE('now') > DATE('start_date', '+20 day')
            """
        overdue_borrowings = self.fetch_one(overdue_borrowings_query, (email,))
        if overdue_borrowings is not None:
            overdue_borrowings = overdue_borrowings[0]
        else:
            overdue_borrowings = 0
        
        return total_borrowed, current_borrowed, overdue_borrowings
    
    def get_penalty_info(self, email):
        penalty_query = """SELECT 
            COUNT(pid) AS total_penalties, 
            IFNULL(SUM(amount - IFNULL(paid_amount, 0)), 0) AS total_outstanding
            FROM penalties
            INNER JOIN borrowings ON penalties.bid = borrowings.bid
            INNER JOIN books ON books.book_id = borrowings.book_id
            WHERE borrowings.member = ? AND IFNULL(paid_amount, 0) < amount AND amount > 0;
            """
        penalty_info = self.fetch_one(penalty_query, (email,))
        return penalty_info # No need to handle Null here as we are doing it in the query itself
    
    # Returns a users penatlies
    def get_penalties(self, email):
        query = """
            SELECT pid, books.title, borrowings.bid, amount, IFNULL(paid_amount, 0)
            FROM penalties, books
            INNER JOIN borrowings ON penalties.bid = borrowings.bid
            WHERE borrowings.member = ? AND (IFNULL(paid_amount, 0) < amount)
            AND (books.book_id = borrowings.book_id) AND (0 < amount)
            """
        penalties = self.fetch_all(query, (email,))
        return penalties
    
    # Deletes penalty, used when payment matches exactly
    def pay_penalty_in_full(self, pid):
        query = """
            DELETE FROM penalties
            WHERE pid = ?
            """
        self.execute_query(query, (pid,))
        
    # Updates penalty entries with new partial payment
    def pay_pentalty_partially(self, pid, payment, paid_amount):
        query = """
            UPDATE penalties
            SET paid_amount = ?
            WHERE pid = ?
            """
        self.execute_query(query, (paid_amount + payment, pid))