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

