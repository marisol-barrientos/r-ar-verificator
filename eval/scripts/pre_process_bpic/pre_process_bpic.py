import pandas as pd
import os

from dotenv import load_dotenv


load_dotenv()
HOME_PATH = os.environ['HOME_PATH']

# Path to the folder containing input CSV files
input_folder = HOME_PATH + "/eval/data/input/logs/bpic2020_original/"

# Path to the folder for saving the output CSV file
output_folder = HOME_PATH + "/eval/data/input/logs/BPIC/"

# List of Excel files
csv_files = [
    "DomesticDeclarations.csv",
    "InternationalDeclarations.csv",
    "PermitLog.csv",
    "PrepaidTravelCost.csv",
    "RequestForPayment.csv"
]

# Columns to include
columns_to_include = [
    "concept:event",
    "concept:instance",
    "org:resource",
    "concept:name",
    "time:timestamp",
    "org:role",
    "document"
]

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame(columns=columns_to_include)

# Custom function to process "concept:name" column
def process_concept_name(value):
    value = value.lower()
    if "by" in value:
        value = value.split("by")[0].strip()
    return value

# Custom function to filter dates
def filter_dates(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: x.split('+')[0])
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    df = df.dropna(subset=[column_name])  # Drop rows with invalid datetime values
    return df[(df[column_name].dt.year == 2017) | (df[column_name].dt.year == 2018) | (df[column_name].dt.year == 2019) & (df[column_name].dt.month.isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))]

# Iterate through the CSV files, read and merge the data
for file in csv_files:
    if not os.path.isfile(file):
        print(f"File '{file}' not found. Skipping.")
        continue

    # Read the CSV file, only including the specified columns
    data = pd.read_csv(file, usecols=lambda col: col.lower() in columns_to_include)

    # Convert all-pet-overview-gpt_4-rcr values to lowercase
    data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # Modify the "concept:name" column values
    data["concept:name"] = data["concept:name"].apply(process_concept_name)

    # Include name of origin file
    data["document"] = file[:-4]

    # Filter rows based on the date
    data = filter_dates(data, "time:timestamp")

    # Append the data to the merged_data DataFrame
    merged_data = merged_data.append(data)

# Reset the index of the merged_data DataFrame
merged_data.reset_index(drop=True, inplace=True)

# Create output path
output_path = os.path.join(output_folder, "BPIC_event_log.csv")

# Save the merged data to a new CSV file
merged_data.to_csv(output_path, index=False)

print("BPIC pre-processed file generated: 'BPIC_event_log.csv'.")