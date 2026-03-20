from datetime import timedelta
import datetime

class Scans:
    def __init__(self, scan_id, scheduler):
        self.data = scheduler.patients_data.query(f"`scan_id` == '{scan_id}'")
        assert scan_id in self.data['scan_id'].unique(), f'There is no scan with id {scan_id}.'
        self.scan_id = self.data['scan_id'].item()
        self.patient = self.data['patient_name'].item()
        self.scan_type = self.data['scan_type'].item()
        self.duration = scheduler.durations.get(self.scan_type, 20)
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