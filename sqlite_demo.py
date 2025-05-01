import sqlite3
import json, datetime
from schedule_item import ScheduleItem

class ScheduleDB:
    def __init__(self, db_name="schedule_item.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the schedule_item table if it doesn't exist"""
        with self.conn:
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS schedule_item (
                    title TEXT NOT NULL,
                    description TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    priority_level TEXT NOT NULL,
                    repetition_days TEXT
                )
            """)

    def insert_item(self, item):
        with self.conn:
            self.c.execute("INSERT INTO schedule_item VALUES (?, ?, ?, ?, ?, ?)", 
                (item.title, 
                item.description, 
                item.start_time.isoformat(), 
                item.end_time.isoformat(), 
                item.priority_level.name,
                json.dumps(item.repetition_days)
                )
            ) 

    def delete_item(self, title):
        with self.conn:
            self.c.execute("DELETE from schedule_item WHERE title = ?", (title,))

if __name__ == "__main__":
    db = ScheduleDB()
    db.conn.close()