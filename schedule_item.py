from enum import Enum

priority_level_enum = Enum('priority_level', ['High', 'Medium', 'Low'])

class ScheduleItem():
    def __init__(self, title, description, start_date, end_date, priority_level, repetition, repetition_days=None):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.priority_level = self.priority_level_decider(priority_level)
        self.repetition = repetition
        self.repetition_days = repetition_days
    
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