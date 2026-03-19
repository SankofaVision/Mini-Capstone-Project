from datetime import datetime

class Patient:
    def __init__(self, name, gender, age, urgency, arrival_time):
        self.name = name
        self.gender = gender
        self.age = age
        self.urgency = urgency
        self.arrival_time = datetime.strptime(arrival_time, "%H:%M")

    def get_priority(self):
        """Convert urgency to a number (lower = more urgent)"""
        if self.urgency == "Critical":
            return 1
        elif self.urgency == "High":
            return 2
        elif self.urgency == "Medium":
            return 3
        else:
            return 4  # Low

    def __repr__(self):
        return f"{self.name} ({self.urgency})"