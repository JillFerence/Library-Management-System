from datetime import datetime, timedelta

"""
******************************
PENALTY MANAGER CLASS
******************************
"""
class PenaltyManager:
    # Initialization method for the Penalty Manager class
    def __init__(self, db_handler):
        self.db = db_handler
    
    # Method to calculate the penalty of an overdue return
    def calculate_penalty(self, start_date):
        # Check for either format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS.SSSSSS'
        if len(start_date) > 10:
            start_date_only = start_date.split(" ")[0]
            deadline = datetime.strptime(start_date_only, "%Y-%m-%d") + timedelta(days=20)
            overdue_days = (datetime.now().date() - deadline.date()).days
            return max(0, overdue_days * 1) # $1 per day
        else:
            deadline = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=20)
            overdue_days = (datetime.now().date() - deadline.date()).days
            return max(0, overdue_days * 1)