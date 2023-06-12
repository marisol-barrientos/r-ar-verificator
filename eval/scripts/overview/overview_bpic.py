import pandas as pd
import re
import os


# Path to the folder for saving the output CSV file
input_file = "/home/marisolbarrientosmoreno/Desktop/SS_23/HiWi/r-ar-verificator/eval/data/output/step_two/pre_processed_bpic.csv"

# Path to the folder for saving the output CSV file
output_folder = "/home/marisolbarrientosmoreno/Desktop/SS_23/HiWi/r-ar-verificator/eval/data/output/overview"

# Load the data
df = pd.read_csv(input_file)

# Create a new column that represents the pair 'org:role' and 'concept:name'
df['pair'] = df['org:role'] + "," + df['concept:name']

# Group the dataframe by document
grouped = df.groupby('document')

# Initialize an empty dictionary to store the pair percentages for each document
pair_percentages_by_document = {}

# Iterate over each group
for name, group in grouped:
    # Count the occurrence of each pair in this group
    pair_counts = group['pair'].value_counts()
    # Calculate the percentage of each pair in this group
    pair_percentages = pair_counts / len(group) * 100
    # Store the percentages in the dictionary
    pair_percentages_by_document[name] = pair_percentages

# Convert the dictionary to a string for further processing
data = ""
for document, pair_percentages in pair_percentages_by_document.items():
    data += f"Document: {document}\n"
    data += pair_percentages.to_string() + "\n"

# Split into sections
sections = re.split("Document: ", data)[1:]  # skip the first empty string

# Initialize an empty dataframe to store the final result
final_df = None

# Loop over each section
for section in sections:
    # Get the document number
    document_number, section_data = section.split("\n", 1)

    # Split into lines
    lines = section_data.strip().split("\n")[1:-1]  # skip the 'pair' line and the last line

    # Initialize lists to store pairs and their values
    resources = []
    activities = []
    values = []

    # Loop over each line
    for line in lines:
        # Split into pair and value
        pair, value = line.rsplit(maxsplit=1)
        resource, activity = pair.split(",")
        resources.append(resource)
        activities.append(activity)
        values.append(float(value))

    # Create a dataframe for this section
    df = pd.DataFrame({document_number: values},
                      index=pd.MultiIndex.from_arrays([resources, activities], names=["Resource", "Activity"]))

    # Merge this dataframe with the final dataframe
    if final_df is None:
        final_df = df
    else:
        final_df = final_df.join(df, how='outer')

# Reset the index and rename the index columns
final_df.reset_index(inplace=True)

# Create output path
output_path = os.path.join(output_folder, "overview_bpic.csv")

# Save the final dataframe as a CSV file
final_df.to_csv(output_path, index=False)
