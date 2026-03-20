from datetime import datetime

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