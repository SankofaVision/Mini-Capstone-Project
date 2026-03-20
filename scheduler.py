import pandas as pd
from datetime import datetime
import numpy as np


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
