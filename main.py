# Import Libraries
import pandas as pd
import numpy as np
import argparse
from datetime import datetime
#Workflow

class Scheduler:
    durations = {"MRI": 90, "CT Scan": 30, "X-Ray": 15, "Ultrasound": 60, "PET Scan": 240}

    def __init__(self, csv_path, resources=None):
        self.csv_path = csv_path
        self.patients_data = None
        self.resources = resources or {"MRI": 2, "CT Scan": 3, "X-Ray": 2, "Ultrasound": 1, "PET Scan": 2}

    def load_data(self):
        assert self.csv_path.endswith('.csv'), f"Expected csv file not {self.csv_path.split('.')[-1]}."
        self.patients_data = pd.read_csv(self.csv_path)
        self.patients_data.columns = [col.lower() for col in self.patients_data.columns]

        expected_columns = ['scan_id', 'patient_name', 'gender', 'age', 'scan_type', 'urgency',
                            'arrival_time', 'wait_time_min', 'status']
        missing = set(expected_columns) - set(self.patients_data.columns)
        assert not missing, f"Missing required columns: {missing}"
        self.patients_data['arrival_time'] = pd.to_datetime(self.patients_data['arrival_time'], format="%H:%M")

    def prioritise_queue(self):
        urgency_order = pd.CategoricalDtype(['Critical', 'High', 'Medium', 'Low'], ordered=True)
        self.patients_data['urgency'] = self.patients_data['urgency'].astype(urgency_order)
        self.patients_data = self.patients_data.sort_values(['scan_type', 'urgency', 'arrival_time'])

    def calculate_wait_times(self):
        self.prioritise_queue()
        pending = self.patients_data[self.patients_data['status'] == 'Pending'].copy()
        other = self.patients_data[self.patients_data['status'] != 'Pending'].copy()
        other['wait_time_min'] = np.nan
        pending['scan_duration'] = pending['scan_type'].map(self.durations)

        def simulate_group(group):
            scan_type = group.name
            num_machines = self.resources.get(scan_type, 1)
            duration = self.durations.get(scan_type, 20)
            wait_times = []
            for i in range(len(group)):
                batch = i // num_machines
                wait_times.append(duration * batch)

            group['wait_time_min'] = wait_times
            return group

        if not pending.empty:
            pending = pending.groupby('scan_type', group_keys=False).apply(simulate_group)
            pending.drop(columns='scan_duration', inplace=True)

        self.patients_data = pd.concat([pending, other], ignore_index=True)

    def set_scan_status(self, scan_id, status):
        assert status in ['Pending', 'In Progress', 'Completed', 'Cancelled'], \
            "Invalid status value. Must be one of ['Pending', 'In Progress', 'Completed', 'Cancelled']"
        self.patients_data.loc[self.patients_data['scan_id'] == scan_id, 'status'] = status
        self.calculate_wait_times()


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
        help="Path to the CSV file"  # replace with path to csv file
    )

    args = parser.parse_args()

    scheduler = Scheduler(args.file)
    scheduler.load_data()
    scheduler.calculate_wait_times()
    df = scheduler.patients_data

    # df = load_data(args.file)
    df = clean_data(df)
    df = sort_by_urgency(df)

    #create queue
    #prioritise urgent patients 
    #schedule scans
    #calculate waiting times for those whose status is pending


# generate summary statistics from scheduler
#generate charts


if __name__ == "__main__":
    main()
