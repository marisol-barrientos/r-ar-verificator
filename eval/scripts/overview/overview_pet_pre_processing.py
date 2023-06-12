import os
import json
from collections import Counter

def analyze_json_files(directory, output_file):
    total_ids = 0
    total_resources = Counter()
    total_activities = Counter()
    file_count = 0

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_count += 1
            with open(os.path.join(directory, filename), 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data.get("pairs", None), list):
                        print(f"Warning: File {filename} does not contain a list under 'pairs' key.", file=output_file)
                        continue
                    for item in data['pairs']:
                        total_ids += 1
                        total_resources[item['resource']] += 1
                        total_activities[item['activity']] += 1
                except json.JSONDecodeError:
                    print(f"Warning: File {filename} could not be decoded.", file=output_file)

    print(f"Total number of files: {file_count}", file=output_file)
    print(f"Total number of IDs: {total_ids}", file=output_file)
    print(f"Average number of IDs per file: {total_ids/file_count if file_count > 0 else 0}", file=output_file)
    print(f"Average number of different resources: {len(total_resources)/file_count if file_count > 0 else 0}", file=output_file)
    print(f"Average number of different activities: {len(total_activities)/file_count if file_count > 0 else 0}", file=output_file)

# directory where your JSON files are located
directory = '../data/output/0_step_one/all-pet-overview-gpt_4-rcr'  # Replace with your directory
# file to save the output
output_filename = "overview-pet-pre-processing.txt"
with open(output_filename, 'w') as output_file:
    analyze_json_files(directory, output_file)
