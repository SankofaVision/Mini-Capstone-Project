import pandas as pd
from datetime import datetime


class Scheduler:
    def __init__(self, scans):
        """
        scans: list of Scan objects
        """
        self.scans = scans

    def prioritise_queue(self):
        """
        Sort scans based on:
        1. Patient urgency (via Patient.get_priority())
        2. Arrival time
        """
        self.scans.sort(
            key=lambda s: (s.patient.get_priority(), s.patient.arrival_time)
        )

    def run_schedule(self, day_start="08:00"):
        """
        Sequential scheduling where a single machine is used.
        """
        today = self.scans[0].patient.arrival_time.date()
        current_time = datetime.strptime(day_start, "%H:%M").replace(
            year=today.year, month=today.month, day=today.day
        )

        for scan in self.scans:
            patient = scan.patient
            start_time = max(current_time, patient.arrival_time)
            scan.start_scan(start_time)
            current_time = scan.end_time

    def get_results(self):
        """
        Convert results to DataFrame for analysis/visualization
        """
        data = []
        for scan in self.scans:
            data.append({'scan_id': scan.scan_id, 'patient_name': scan.patient.name, 'scan_type': scan.scan_type,
                         'urgency': scan.patient.urgency, 'arrival_time': scan.patient.arrival_time.time(),
                         'start_time': scan.start_time.time() if scan.start_time else None,
                         'end_time': scan.end_time.time() if scan.end_time else None,
                         'wait_time_min': round(scan.get_wait_time(), 1)
                         })

        return pd.DataFrame(data)
