#
# This file is part of r-ar-verificator.
#
# r-ar-verificator is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# r-ar-verificator is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with r-ar-verificator (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.
import json
import os
from dotenv import load_dotenv

def evaluate_results(golden_standard_file_path, step_seven_output_file_path, output_name):
    with open(golden_standard_file_path, "r") as f1:
        golden_standard_file = json.load(f1)

    # Load the second JSON
    with open(step_seven_output_file_path, "r") as f2:
        step_seven_output_file = json.load(f2)

    # Initialize the output JSON structure
    output_json = {
        "true_negative": [],
        "true_positive": [],
        "false_positive": [],
        "false_negative": [],
    }

    golden_standard_file_compliant_output = []
    golden_standard_file_non_compliant_output = []

    step_seven_output_file_compliant_output = []
    step_seven_output_file_non_compliant_output = []

    for case_id in golden_standard_file["compliant_pairs"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                golden_standard_file_compliant_output.append(value.split(',')[0])


    for case_id in golden_standard_file["non_compliant_pairs"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                golden_standard_file_non_compliant_output.append(value.split(',')[0])

    for case_id in step_seven_output_file["compliant_output"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                step_seven_output_file_compliant_output.append(value.split(',')[0])

    for case_id in step_seven_output_file["non_compliant_output"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                step_seven_output_file_non_compliant_output.append(value.split(',')[0])

    # Iterate through the case IDs in the first JSON
    for case_id in golden_standard_file["compliant_pairs"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                if value.split(',')[0] in step_seven_output_file_compliant_output:
                    output_json["true_positive"].append(value.split(',')[0])
                elif value.split(',')[0] in step_seven_output_file_non_compliant_output:
                    output_json["false_negative"].append(value.split(',')[0])

    for case_id in golden_standard_file["non_compliant_pairs"]:
        for key, value_list in case_id['case_id'].items():
            for value in value_list:
                if value.split(',')[0] in step_seven_output_file_non_compliant_output:
                    output_json["true_negative"].append(value.split(',')[0])
                elif value.split(',')[0] in step_seven_output_file_compliant_output:
                    output_json["false_positive"].append(value.split(',')[0])

    # Write the output JSON to a new file
    with open(output_name, "w") as f3:
        json.dump(output_json, f3, indent=4)


def main():
    # Load environment variables from the .env file
    load_dotenv()
    HOME_PATH = os.environ['HOME_PATH']

    golden_standard_file_path_b_c = HOME_PATH + "src/evaluate_results/output/1_step_two/compliant/gold_standard_bicycle_manufacturing.json"
    step_seven_output_file_path_b_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/compliant/bicycle_manufacturing_log_compliant_output.json"
    output_name_b_c = "bicycle_manufacturing_eval_last_step.json"

    golden_standard_file_path_r_c = HOME_PATH + "src/evaluate_results/output/1_step_two/compliant/gold_standard_running_example_v3_log.json"
    step_seven_output_file_path_r_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/compliant/running_example_v3_log_compliant_output.json"
    output_name_r_c = "running_example_v3_eval_last_step.json"

    golden_standard_file_path_s_c = HOME_PATH + "src/evaluate_results/output/1_step_two/compliant/gold_standard_schedule_meetings_creation_next_year.json"
    step_seven_output_file_path_s_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/compliant/schedule_meetings_creation_next_year_log_compliant_output.json"
    output_name_s_c = "schedule_meetings_creation_next_year_eval_last_step.json"

    golden_standard_file_path_b_n_c = HOME_PATH + "src/evaluate_results/output/1_step_two/non_compliant/gold_standard_bicycle_manufacturing.json"
    step_seven_output_file_path_b_n_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/non_compliant/bicycle_manufacturing_log_compliant_output.json"
    output_name_b_n_c = "non_bicycle_manufacturing_eval_last_step.json"

    golden_standard_file_path_r_n_c = HOME_PATH + "src/evaluate_results/output/1_step_two/non_compliant/gold_standard_running_example_v3_log.json"
    step_seven_output_file_path_r_n_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/non_compliant/running_example_v3_log_compliant_output.json"
    output_name_r_n_c = "non_running_example_v3_eval_last_step.json"

    golden_standard_file_path_s_n_c = HOME_PATH + "src/evaluate_results/output/1_step_two/non_compliant/gold_standard_schedule_meetings_creation_next_year.json"
    step_seven_output_file_path_s_n_c = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/non_compliant/schedule_meetings_creation_next_year_log_compliant_output.json"
    output_name_s_n_c = "non_schedule_meetings_creation_next_year_eval_last_step.json"

    evaluate_results(golden_standard_file_path_s_n_c, step_seven_output_file_path_s_n_c, output_name_s_n_c)

if __name__ == "__main__":
    main()