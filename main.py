# Import Libraries
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta
from patient import Patients
from scan import Scans
from scheduler import Scheduler
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # force GUI backend
import matplotlib.dates as mdates

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

#Visualization    
def plots(data):
    """
    Generate and display three visualizations for scan scheduling analysis.

    The function produces:
    1. A bar chart showing the distribution of patients across different scan types.
    2. A line chart illustrating patient wait times throughout the day based on arrival time.
    3. A pie chart representing the proportion of patients by urgency level.

    Parameter
    ----------
    data : pandas.DataFrame
        Specific columns used:
        - 'scan_type' : categorical values indicating the type of scan
        - 'arrival_time' : time values (HH:MM format) representing patient arrival
        - 'wait_time_min' : numerical values indicating wait time in minutes
        - 'urgency' : categorical values representing patient urgency levels

    Returns
    -------
        Displays the generated plots using matplotlib.
    """
    
    plt.figure(figsize=(15, 5))
    
    # Chart 1: Bar Chart 
    plt.subplot(1, 3, 1)
    data['scan_type'].value_counts().plot(kind='bar')
    plt.title('Queue by Scan Type')
    plt.xlabel('Type of Scan')
    plt.ylabel('Patient Count')

    
    # Chart 2: Line Chart 
    plt.subplot(1, 3, 2)
    data['arrival_time'] = pd.to_datetime(data['arrival_time'], format='%H:%M')
    data_sorted = data.sort_values('arrival_time')
    plt.plot(data_sorted['arrival_time'], data_sorted['wait_time_min'], marker='o')
    plt.title('Wait Time Across Day')
    plt.xlabel('Arrival Time')
    plt.ylabel('Minutes')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    
    
    # Chart 3: Pie Chart 
    plt.subplot(1, 3, 3)
    data['urgency'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['red', 'orange', 'yellow', 'green'])
    plt.title('Urgency Priority')
    plt.ylabel('') 
    plt.tight_layout()
    plt.show(block=True)

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
    plots(df)
    



if __name__ == "__main__":
    main()
