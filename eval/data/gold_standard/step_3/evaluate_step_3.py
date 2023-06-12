import json
import os

from dotenv import load_dotenv

load_dotenv()
HOME_PATH = os.environ['HOME_PATH']

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def compare_jsons(output_step_3, gold_standard_json):
    true_positive = 0
    false_positive = 0
    false_negative = 0

    # check for true positives and false positives
    for gold_standard_entry in gold_standard_json:
        for activity_entry in output_step_3['activity_matching_output']:
            if gold_standard_entry['Activity_in_Log'] == activity_entry['Activity_in_Log']:
                if gold_standard_entry['Detected_Activity'] == activity_entry['Detected_Activity']:
                    true_positive += 1
                else:
                    false_positive += 1

    # check for false negatives
    for gold_standard_entry in gold_standard_json:
        if not any(gold_standard_entry['Activity_in_Log'] == activity_entry['Activity_in_Log'] for activity_entry in
                   output_step_3['activity_matching_output']):
            false_negative += 1

    # check for false positives
    for output_step_3_entry in output_step_3['activity_matching_output']:
        if not any(output_step_3_entry['Activity_in_Log'] == activity_entry['Activity_in_Log'] for activity_entry in
                    gold_standard_json):
            false_positive += 1

    return true_positive, false_positive, false_negative

def calculate_metrics(true_positive, false_positive, false_negative):
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = 2 * (recall * precision) / (recall + precision)

    return precision, recall, f1_score

def main():
    scenario = 'BPIC'
    output_step_3_path = HOME_PATH + "/eval/data/gold_standard/step_3/" + scenario + "/0_80_" + scenario + "_activity_check.json"
    gold_standard_path = HOME_PATH + "/eval/data/gold_standard/step_3/" + scenario + "/" + scenario + "_gold_standard_step_3_4.json"

    output_step_3 = read_json(output_step_3_path)
    gold_standard_json = read_json(gold_standard_path)

    true_positive, false_positive, false_negative = compare_jsons(output_step_3, gold_standard_json)

    precision, recall, f1_score = calculate_metrics(true_positive, false_positive, false_negative)

    print(f'True Positives: {true_positive}')
    print(f'False Positives: {false_positive}')
    print(f'False Negatives: {false_negative}')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'F1 Score: {f1_score}')


if __name__ == "__main__":
    main()
