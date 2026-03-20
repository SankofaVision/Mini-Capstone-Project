# Import Libraries
import pandas as pd
import numpy as np
import argparse
from datetime import datetime
# from patient import Patient
# from scan import Scan
# from scheduler import Scheduler

# Create a patient
# p1 = Patient("Patient 1", "Male", 45, "High", "10:00")
#
# # Create a scan
# s1 = Scan("SCN001", p1, "CT Scan")
#
# # Check duration
# print("Duration:", s1.duration)
#
# #Start scan
# current_time = datetime.strptime("10:30", "%H:%M")
# s1.start_scan(current_time)
#
# # Check times
# print("Start Time:", s1.start_time)
# print("End Time:", s1.end_time)
#
# #Check wait time
# print("Wait Time:", s1.get_wait_time())
#
# p2 = Patient("Patient 2", "Female", 60, "Critical", "09:30")
# p3 = Patient("Patient 3", "Male", 30, "Low", "08:45")
# p4 = Patient("Patient 4", "Female", 25, "Medium", "09:00")
#
# s2 = Scan("SCN002", p2, "MRI")
# s3 = Scan("SCN003", p3, "X-Ray")
# s4 = Scan("SCN004", p4, "Ultrasound")
#
# scans = [s1, s2, s3, s4]
# scheduler = Scheduler(scans)
# scheduler.prioritise_queue()
#
# print("Queue after prioritisation:")
# for scan in scheduler.scans:
#     print(f"{scan.scan_id} - {scan.patient.name} ({scan.patient.urgency})")
#
# scheduler.run_schedule(day_start="08:00")
# print("Scheduled Results:")
# for scan in scheduler.scans:
#     print(f"""
# Scan ID: {scan.scan_id}
# Patient: {scan.patient.name}
# Urgency: {scan.patient.urgency}
# Arrival: {scan.patient.arrival_time.time()}
# Start: {scan.start_time.time()}
# End: {scan.end_time.time()}
# Wait Time: {round(scan.get_wait_time(), 1)} minutes
# """)
#
# df = scheduler.get_results()
# print("\nDataFrame View:\n", df)
#
#
# # Data Loading
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     print(df.to_string())
#     return df
#
#
# # Handling missing data
# def clean_data(df):
#     df = df.dropna()
#     return df
#
#
# # Sort by Urgency
# def sort_by_urgency(df):
#     urgency_order = ["Critical", "High", "Medium", "Low"]
#
#     df["urgency"] = pd.Categorical(
#         df["urgency"],
#         categories=urgency_order,
#         ordered=True
#     )
#
#     df = df.sort_values(by="urgency")
#
#     return df


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
        help="Path to the CSV file"  #replace with path to csv file
    )

    args = parser.parse_args()

    df = load_data(args.file)
    df = clean_data(df)
    df = sort_by_urgency(df)


#Workflow

class Scheduler:
    durations = {"MRI": 90, "CT Scan": 30, "X-Ray": 15, "Ultrasound": 60, "PET Scan": 240}
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.patients_data = None
        self.expected_columns = None
        self.resources = None

    def load_data(self):
        assert self.csv_path.endswith('.csv'), f"Expected csv file not {self.csv_path.split('.')[-1]}."
        self.patients_data = pd.read_csv(self.csv_path)
        self.patients_data.columns = [column.lower() for column in self.patients_data.columns]
        self.expected_columns = ['scan_id', 'patient_name', 'gender', 'age', 'scan_type', 'urgency', 'arrival_time',
                                 'wait_time_min', 'status']
        assert not (set(self.expected_columns) - set(self.patients_data.columns)), \
            f'These columns, {set(set(self.expected_columns) - self.patients_data.columns)} are required to be in your data but are missing.'
        self.patients_data['arrival_time'] = pd.to_datetime(self.patients_data['arrival_time'], format="%H:%M")
        in_progress = self.patients_data[self.patients_data['status'] == 'In Progress'].copy()
        self.resources = (in_progress.groupby('scan_type')['scan_id'].nunique().to_dict())

    def prioritise_queue(self):
        # status_order = pd.CategoricalDtype(['Pending', 'In Progress', 'Completed', 'Cancelled'], ordered=True)
        urgency_order = pd.CategoricalDtype(['Critical', 'High', 'Medium', 'Low'], ordered=True)
        self.patients_data['urgency'] = self.patients_data['urgency'].astype(urgency_order)
        self.patients_data = self.patients_data.sort_values(['scan_type', 'urgency', 'arrival_time'])

    def calculate_wait_times(self):
        self.prioritise_queue()
        pending = self.patients_data[self.patients_data['status'] == 'Pending'].copy()
        in_progress = self.patients_data[self.patients_data['status'] == 'In Progress'].copy()
        other = self.patients_data[~self.patients_data['status'].isin(['Pending', 'In Progress'])].copy()
        # other['wait_time_min'] = np.nan
        # in_progress['wait_time_min'] = np.nan
        pending['scan_duration'] = pending['scan_type'].map(self.durations)
        in_progress['scan_duration'] = in_progress['scan_type'].map(self.durations)
        if not pending.empty:
            now = pending['arrival_time'].min()
        else:
            now = pd.Timestamp.now()

        def simulate_group(group):
            scan_type = group.name
            num_machines = self.resources.get(scan_type, 1)
            machines = []
            busy = in_progress[in_progress['scan_type'] == scan_type]
            for _, row in busy.iterrows():
                machines.append(now + timedelta(minutes=row['scan_duration']))
            while len(machines) < num_machines:
                machines.append(now)
            wait_times = []
            for _, row in group.iterrows():
                arrival = row['arrival_time']
                duration = row['scan_duration']

                idx = np.argmin(machines)
                available_time = machines[idx]

                start_time = max(arrival, available_time)
                wait = (start_time - arrival).total_seconds() / 60
                wait_times.append(wait)

                machines[idx] = start_time + timedelta(minutes=duration)

            group['wait_time_min'] = wait_times
            return group

        if not pending.empty:
            pending = pending.groupby('scan_type', group_keys=False).apply(simulate_group)
            pending.drop(columns='scan_duration', inplace=True)

        self.patients_data = pd.concat([pending, in_progress, other], ignore_index=True)

    def set_scan_status(self, scan_id, status):
        assert status in ['Pending', 'In Progress', 'Completed', 'Cancelled'], "Invalid status value passed. Expecting one of ['Pending', 'In Progress', 'Completed', 'Cancelled']"
        self.patients_data.loc[self.patients_data['scan_id'] == scan_id, 'status'] = status
        self.compute_wait_times()


class Patients:
    def __init__(self, name, scheduler):
        self.scheduler = scheduler
        self.data = self.scheduler.patients_data.query(f"`patient_name` == '{name}'")
        assert name in self.data['patient_name'].unique(), f'Patient with name {name} does not exist in database.'
        self.name = name
        self.age = self.data.iloc[0]['age'].item()
        self.urgency = self.data['urgency'].item() if self.data.shape[0] == 1 else self.data[['scan_type', 'urgency']].to_dict()
        self.gender = self.data.iloc[0]['gender'].item()
        self.arrival_time = self.data.iloc[0]['arrival_time'].item()
        self.wait_time = self.data['wait_time_min'].item() if self.data.shape[0] == 1 else self.data[['scan_type', 'wait_time_min']].to_dict()

    def update_status(self, new_status):
        self.scheduler.patients_data.loc[self.scheduler.patients_data['patient_name'] == self.name, 'status'] = new_status


class Scans:
    def __init__(self, scan_id, scheduler):
        self.data = scheduler.patients_data.query(f"`scan_id` == '{scan_id}'")
        assert scan_id in self.data['scan_id'].unique(), f'There is no scan with id {scan_id}.'
        self.scan_id = self.data['scan_id'].item()
        self.patient = self.data['patient_name'].item()
        self.scan_type = self.data['scan_type'].item()
        self.duration = scheduler.durations.get(scan_type, 20)
        self.start_time = None
        self.end_time = None
        self.wait_time = None

    def start_end_time(self):
        self.wait_time = self.data['wait_time_min'].item()
        self.start_time = datetime.strptime(self.data['arrival_time'], "%H:%M") + timedelta(minutes=self.wait_time)
        self.end_time = self.start_time + timedelta(minutes=self.duration)

    def __repr__(self):
        self.start_end_time()
        return f"{self.scan_id}: {self.scan_type} for patient {self.patient} scheduled from {self.start_time} to {self.end_time}."


    #create queue
    #prioritise urgent patients 
    #schedule scans
    #calculate waiting times for those whose status is pending


# generate summary statistics from scheduler
#generate charts


if __name__ == "__main__":
    main()
