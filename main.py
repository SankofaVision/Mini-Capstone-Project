# Import Libraries
import pandas as pd
import argparse
from datetime import datetime
from patient import Patient
from scan import Scan
from scheduler import Scheduler

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

p2 = Patient("Patient 2", "Female", 60, "Critical", "09:30")
p3 = Patient("Patient 3", "Male", 30, "Low", "08:45")
p4 = Patient("Patient 4", "Female", 25, "Medium", "09:00")

s2 = Scan("SCN002", p2, "MRI")
s3 = Scan("SCN003", p3, "X-Ray")
s4 = Scan("SCN004", p4, "Ultrasound")

scans = [s1, s2, s3, s4]
scheduler = Scheduler(scans)
scheduler.prioritise_queue()

print("Queue after prioritisation:")
for scan in scheduler.scans:
    print(f"{scan.scan_id} - {scan.patient.name} ({scan.patient.urgency})")

scheduler.run_schedule(day_start="08:00")
print("Scheduled Results:")
for scan in scheduler.scans:
    print(f"""
Scan ID: {scan.scan_id}
Patient: {scan.patient.name}
Urgency: {scan.patient.urgency}
Arrival: {scan.patient.arrival_time.time()}
Start: {scan.start_time.time()}
End: {scan.end_time.time()}
Wait Time: {round(scan.get_wait_time(), 1)} minutes
""")

df = scheduler.get_results()
print("\nDataFrame View:\n", df)


# Data Loading
def load_data(file_path):
    df = pd.read_csv(file_path)
    print(df.to_string())
    return df


# Handling missing data
def clean_data(df):
    df = df.dropna()
    return df


# Sort by Urgency
def sort_by_urgency(df):
    urgency_order = ["Critical", "High", "Medium", "Low"]

    df["urgency"] = pd.Categorical(
        df["urgency"],
        categories=urgency_order,
        ordered=True
    )

    df = df.sort_values(by="urgency")

    return df


#  Summary Statistics
def summary_stats(df):
    print("\n--- SUMMARY STATISTICS ---")

    print(f"Total Requests       : {len(df)}")
    print(f"Average Wait Time    : {df['wait_time_min'].mean():.2f} minutes")

    print("\nWait Time Range:")
    print(f"Min  : {df['wait_time_min'].min()} minutes")
    print(f"Max  : {df['wait_time_min'].max()} minutes")

    print("\nScan Type Distribution:")
    print(df["scan_type"].value_counts().to_string())


def main():
    parser = argparse.ArgumentParser(description="Scan Scheduling & Queue Manager")

    parser.add_argument(
        "file",
        type=str,
        help="Path to the CSV file"
    )

    args = parser.parse_args()

    df = load_data(args.file)
    df = clean_data(df)
    df = sort_by_urgency(df)

    summary_stats(df)


if __name__ == "__main__":
    main()
