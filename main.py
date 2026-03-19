# Import Libraries
import pandas as pd
import argparse

# Data Loading
def load_data(file_path):
    df = pd.read_csv(file_path)
    print(df.to_string())
    return df


# Handling missing data
def clean_data(df):
    df = df.dropna()
    return df


# Sort by Urgency
def sort_by_urgency(df):
    urgency_order = ["Critical", "High", "Medium", "Low"]

    df["urgency"] = pd.Categorical(
        df["urgency"],
        categories=urgency_order,
        ordered=True
    )

    df = df.sort_values(by="urgency")

    return df


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

    df = load_data(args.file)
    df = clean_data(df)
    df = sort_by_urgency(df)

    summary_stats(df)



if __name__ == "__main__":
    main()