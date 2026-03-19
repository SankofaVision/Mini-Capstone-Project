from datetime import datetime
from patient import Patient
from scan import Scan

# Create a patient
p1 = Patient("Patient 1", "Male", 45, "High", "10:00")

# Create a scan
s1 = Scan("SCN001", p1, "CT Scan")

# Check duration
print("Duration:", s1.duration)

#Start scan
current_time = datetime.strptime("10:30", "%H:%M")
s1.start_scan(current_time)

# Check times
print("Start Time:", s1.start_time)
print("End Time:", s1.end_time)

#Check wait time
print("Wait Time:", s1.get_wait_time())