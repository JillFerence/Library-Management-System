import sqlite3
from sqlite3 import Error
import datetime

"""
******************************
DATABASE HANDLER CLASS
******************************
"""
class DatabaseHandler:
    # Initialization method for the database handler class
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.shown_book_ids = [] # List of book ids that are currently displayed
    
    """
    ******************************
    HELPER DB METHODS
    ******************************
    """

    # Creates the connection for sqlite3
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    # Method for executing a query
    def execute_query(self, query, params):
        try:
            c = self.conn.cursor()
            c.execute(query, params)
            self.conn.commit()
            return c
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    # Method for fetching a single record of a query result
    def fetch_one(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchone()
        else:
            return None
    
    # Method for fetching all the rows of a query result
    def fetch_all(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchall()
        else:
            return []
    
    # Closes the connection for sqlite3
    def close_connection(self):
        status = self.conn.close()
        if status:
            print("Connection closed")
        else:
            print("Connection is already closed")
    
    """
    ******************************
    MEMBER PROFILE DB METHODS
    ******************************
    """

    # Gets the member personal information from the database
    def get_member_info(self, email):
        query = "SELECT name, email, byear FROM members WHERE email = ?"
        return self.fetch_one(query, (email,))
    
    # Gets the member borrowing information from the database
    def get_borrowing_info(self, email):
        # Previous borrowings
        borrow_query = "SELECT COUNT(*) FROM borrowings WHERE member = ?"
        total_borrowed = self.fetch_one(borrow_query, (email,))
        if total_borrowed is not None:
            total_borrowed = total_borrowed[0]
        else:
            total_borrowed = 0
        # Current borrowings
        current_borrow_query = "SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL"
        current_borrowed = self.fetch_one(current_borrow_query, (email,))
        if current_borrowed is not None:
            current_borrowed = current_borrowed[0]
        else:
            current_borrowed = 0
        # Overdue borrowings
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

    """
    ******************************
    PAY PENALTY DB METHODS
    ******************************
    """

    # Gets the member penalty information from the database
    def get_penalty_info(self, email):
        penalty_query = """
            SELECT COUNT(*), IFNULL(SUM(amount - IFNULL(paid_amount, 0)), 0)
            FROM penalties
            INNER JOIN borrowings ON penalties.bid = borrowings.bid
            WHERE borrowings.member = ? AND (paid_amount IS NULL OR paid_amount < amount)
            """
        penalty_info = self.fetch_one(penalty_query, (email,))
        return penalty_info # No need to handle Null here as we are doing it in the query itself
    
    # Returns a users penalties
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

    """
    ******************************
    BOOK SEARCH DB METHODS
    ******************************
    """

    # Retrieves all books with the title or author containing a given keyword
    def get_book_search_info(self, keyword, limit, page = 1):
        offset = (page - 1) * limit # Offset for the query to handle paginatio and skip that many rows
        script = """
        -- system must display book id, title, author, publish year, average rating, and whether the book is available or on borrow
        SELECT k.book_id, k.title, k.author, k.pyear AS publish_year, AVG(r.rating) AS average_rating,
            -- whether the book is available (is not in borrowings) or on borrow (is in borrowings)
            CASE 
                WHEN b.book_id IS NULL THEN 'Available'
                ELSE 'On Borrow'
            END AS availability
        FROM
            books k
        -- join books and reviews to get books with reviews               
        LEFT JOIN 
            reviews r ON k.book_id = r.book_id
        -- join books and borrowings, consider only current borrowings for 'On Borrow' where the end date is ahead of the current date
        LEFT JOIN 
            borrowings b ON k.book_id = b.book_id AND (b.end_date > DATETIME('now') OR b.end_date IS NULL)
        -- retrive books in which the title or author contain the keyword 
        -- '%' || ? || '%' = 0 or more characters + keyword + 0 or more characters
        WHERE 
            k.title LIKE '%' || ? || '%' OR
            k.author LIKE '%' || ? || '%' 
        GROUP BY 
            k.book_id, k.title, k.author, k.pyear 
        -- sorted as books w/ matching title first (ascending order), books w/ matching author second(ascending order)
        ORDER BY k.title, k.author  
        -- only return 5 books at each request
        LIMIT ? 
        -- skip a number of rows to show more books
        OFFSET ?
        """
        books = self.fetch_all(script, (keyword, keyword, limit, offset))
        self.shown_book_ids.extend([str(book[0]) for book in books]) 
        return books
    
    # Checks if the book id is a valid book id in the book list
    def check_book_id_validity(self, book_id):
        query = "SELECT COUNT(*) FROM books k WHERE k.book_id = ?"
        counts = self.fetch_one(query, (book_id,))
        if counts[0] == 0:
            return False
    
    # Checks if the book id is in the search list that was displayed to the user
    def check_book_id_in_list(self, book_id):
        return book_id in self.shown_book_ids
    
    # Checks the availability of the book
    def check_book_id_availability(self, book_id):
        # If the book is not available to borrow
        query = "SELECT COUNT(*) FROM borrowings b WHERE b.book_id = ? AND (end_date > DATETIME('now') OR end_date IS NULL)"
        counts = self.fetch_one(query, (book_id,))
        if counts[0] > 0:
            return False
        # If the book is available to borrow
        else:
            return True
    
    # If a member borrowed a book, assigns a unique number to bid and sets the today’s date as start date
    def borrow_book(self, email, book_id):
        start_date = datetime.datetime.now()
        end_date = None
        query = "INSERT INTO borrowings (member, book_id, start_date, end_date) VALUES (?, ?, ?, ?)"
        borrowed = self.execute_query(query, (email, book_id, start_date, end_date))