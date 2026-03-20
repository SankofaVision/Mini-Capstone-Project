# Import Libraries
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta
from patient import Patients
from scan import Scans
from scheduler import Scheduler

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

    scheduler = Scheduler(args.file)
    scheduler.load_data()
    scheduler.calculate_wait_times()
    df = scheduler.patients_data



if __name__ == "__main__":
    main()
