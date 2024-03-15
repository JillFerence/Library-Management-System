from db.db_handler import DatabaseHandler
from auth.auth import Auth
from ui.ui import UI
import sys

def main():

    try: 
        db_path = sys.argv[1]
    except IndexError:
        print("Improper code usage, please use: \npython3 main.py \"database\"")
        sys.exit(1)
    
    db = DatabaseHandler(db_path)
    auth = Auth(db)

    ui = UI(auth)

    ui.show_start_menu()

if __name__ == "__main__":
    main()