from datetime import timedelta

class Scan:
    DURATIONS = {
        "MRI": 90,
        "CT Scan": 30,
        "X-Ray": 15,
        "Ultrasound": 60,
        "PET Scan": 240
    }

    def __init__(self, scan_id, patient, scan_type):
        self.scan_id = scan_id
        self.patient = patient
        self.scan_type = scan_type
        self.duration = self.DURATIONS.get(scan_type, 20)
        self.start_time = None
        self.end_time = None

    def start_scan(self, current_time):
        """Start the scan"""
        self.start_time = current_time
        self.end_time = current_time + timedelta(minutes=self.duration)

    def get_wait_time(self):
        """Calculate how long patient waited"""
        if self.start_time:
            wait = self.start_time - self.patient.arrival_time
            return wait.total_seconds() / 60  # minutes
        return 0

    def __repr__(self):
        return f"{self.scan_id} - {self.scan_type}"