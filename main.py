from schedule_item import *
import datetime

def main():
    j = ScheduleItem("LOl", "LOL", datetime.datetime(2025, 4, 16, 13, 30, 45), datetime.datetime(2025, 4, 16, 13, 45, 45), 1, True, [1])
    
    print(j)
if __name__ == "__main__":
    main()
