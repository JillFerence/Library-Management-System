from db.db_handler import DatabaseHandler
from auth.auth import Auth
from ui.ui import UI
from managers.borrowing_manager import BorrowingManager
from managers.book_manager import BookManager
from managers.penalty_manager import PenaltyManager
from managers.profile_manager import ProfileManager
import sys


def main():

    try: 
        db_path = sys.argv[1]
    except IndexError:
        print("Improper code usage, please use: \npython3 main.py \"database\"")
        sys.exit(1)
    
    db = DatabaseHandler(db_path)
    auth = Auth(db)

    borrowing_manager = BorrowingManager(db)
    book_manager = BookManager(db)
    penalty_manager = PenaltyManager(db)
    profile_manager = ProfileManager(db)


    ui = UI(auth, borrowing_manager, book_manager, penalty_manager, profile_manager)

    ui.show_start_menu()

if __name__ == "__main__":
    main()