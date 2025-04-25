from schedule_item import *
import datetime
from sqlite_demo import *
def main():
    db = ScheduleDB()
    db.c.execute("SELECT * FROM schedule_item")
    print(db.c.fetchall())
    print("it workds")
    
    
if __name__ == "__main__":
    main()
