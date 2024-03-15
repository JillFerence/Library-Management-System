from datetime import datetime, timedelta

class PenaltyManager:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def calculate_penalty(self, start_date):
        deadline = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=20)
        overdue_days = (datetime.now().date() - deadline.date()).days
        return max(0, overdue_days * 1) # $1 per day