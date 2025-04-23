from enum import Enum
import datetime

priority_level_enum = Enum('priority_level', ['High', 'Medium', 'Low'])

class ScheduleItem():
    def __init__(self, title, description, start_date, end_date, priority_level, repetition, repetition_days=None):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.correct_start_and_end_date(start_date, end_date)
        self.priority_level = self.priority_level_decider(priority_level)
        self.repetition = repetition
        if repetition:
            self.repetition_days = self.repetition_convertor(repetition_days)
    
    def priority_level_decider(self, priority_level):
        if isinstance(priority_level, str):
            try:
                priority_level = priority_level_enum[priority_level]
            except KeyError:
                raise ValueError(f"Invalid priority level: '{priority_level}'. Must be 'High', 'Medium', or 'Low'")
        
        elif isinstance(priority_level, int):
            if priority_level == 1:
                priority_level = priority_level_enum.High
            elif priority_level == 2:
                priority_level = priority_level_enum.Medium
            elif priority_level == 3:
                priority_level = priority_level_enum.Low
            else:
                raise ValueError("Priority level must be 1 (High), 2 (Medium), or 3 (Low)")
        
        if priority_level not in priority_level_enum.__members__.values():
            raise ValueError("Priority level must be one of: High, Medium, Low")
        
        return priority_level
    
    def correct_start_and_end_date(self, start_date, end_date):
        if isinstance(end_date, datetime.datetime) and isinstance(start_date, datetime.datetime):
            if end_date < start_date:
                raise ValueError("End date must be after starting date")
            return
        raise ValueError("Wrong type for date")
    
    def repetition_convertor(self, repetition_days):
        if repetition_days == "daily":
            return [0, 1, 2, 3, 4, 5, 6]
        
        if repetition_days == "once a week":
            day_of_the_week = self.start_date.weekday()
            return [day_of_the_week]
        
        if isinstance(repetition_days, list):
            for day in repetition_days:
                if day < 0 or day > 6:
                    raise ValueError("Repetition days need to be in a list from 0-6")

            return repetition_days
        raise ValueError("Wrong format, not a list or a Keyword")
    
    def start_to_end_date(self):
        deltatime = self.end_date - self.start_date
        return deltatime
    
    def is_event_active(self):
        if datetime.datetime.now() > self.start_date and self.end_date > datetime.datetime.now():
            return True
        return False
        
    def next_event(self):
        now = datetime.datetime.now()
        #Event that already ended/started and doesnt repeat
        if self.repetition == False and self.start_date < now:
            return False
        #Event that does not repeat, but still hasnt started
        if self.start_date > now:
            return self.start_date - now
        if not self.repetition_days:
            return False
        
        till_today = 0
        days_till_today = 0

        #Calculating the difference in days
        today = now.weekday()
        if self.end_date < now:
            days_till_today = (datetime.datetime.today().date() - self.start_date.date()).days
        
        #Calculating day difference for event, We need to check if the event is today or not
        till_today = self.start_date + datetime.timedelta(days=days_till_today)
        
        for days in sorted(self.repetition_days):
            if today > days:
                continue

            if today < days:
                till_next = till_today + datetime.timedelta(days=(days - today))
                return till_next - now
            
            if today == days:
                if till_today - now > datetime.timedelta(0):
                    return till_today - now
                continue
        #Events that are next week
        return till_today - now + datetime.timedelta(days=7-(today-min(self.repetition_days)))
    
    def __str__(self):
        return f"{self.title}: {self.start_date.strftime('%Y-%m-%d %H:%M')} to {self.end_date.strftime('%Y-%m-%d %H:%M')} Priority: {self.priority_level}"