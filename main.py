import pandas as pd


class Scheduler:
    def __init__(self, patients_file_path):
        self.patients_file = patients_file_path
        assert self.patients_file.split('.')[-1] in ['csv', 'xlsx'], 'File should be in Excel format with extension .csv or .xlsx'
        self.patients_data = pd.read_csv(self.patients_file) if self.patients_file.endswith('.csv') else pd.read_excel(self.patients_file)
        self.patients_data.columns = [column.lower() for column in self.patients_data.columns]
        self.expected_columns = ['scan_id', 'patient_name', 'gender', 'age', 'scan_type', 'urgency', 'arrival_time', 'wait_time_min', 'status']
        assert set(self.patients_data.columns) - set(self.expected_columns),\
            f'These columns, {set(self.patients_data.columns) - set(self.expected_columns)} are required to be in your data but are missing.'




