import json
import os

from dotenv import load_dotenv

load_dotenv()
HOME_PATH = os.environ['HOME_PATH']
scenario = 'SM'

# Load gold standard
with open(HOME_PATH + "/eval/data/gold_standard/step_4_5/" +  scenario + "/" + scenario + "_gold_standard_step_3_4.json") as f:
    gold_standard = json.load(f)

# Load output
with open(HOME_PATH + "/eval/data/gold_standard/step_4_5/" + scenario + "/0_80_" + scenario + "_default_compliant_output.json") as f:
    output = json.load(f)

# Convert the gold standard to a dictionary for easier lookup
gold_dict = {item['Detected_Activity']: item for item in gold_standard}

# Initialize counters
true_positives = 0
false_negatives = 0
false_positives = 0

# Iterate over the output data
for output_item in output['default_compliance_check_output']:
    matched_activity = output_item.get('Matched_activity')

    # If the matched activity is in the gold standard, compare the items
    if matched_activity and matched_activity in gold_dict:
        gold_item = gold_dict[matched_activity]

        if gold_item['Resources'].lower() == output_item['Resource_Log'].lower():
            if output_item['Compliant']:
                true_positives += 1
            else:
                false_negatives += 1
        else:
            if not output_item['Compliant']:
                true_positives += 1
            else:
                false_positives += 1

# Compute Precision, Recall, and F1 Score
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1_score = 2 * ((precision * recall) / (precision + recall))

print(f'True positives: {true_positives}')
print(f'False negatives: {false_negatives}')
print(f'False positives: {false_positives}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1_score}')
