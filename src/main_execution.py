"""
This file is used to execute to whole process in a chronological order
"""

import os
import sys
import json

from dotenv import load_dotenv

sys.path.append('pre_processing/event_log')
sys.path.append('compliance_verification')

from pre_processing.textual_description.gpt_4.add_resource_patterns import detect_and_add_patterns
from src.pre_processing.event_log.pre_process_event_log_generator import create_event_log_pre_process_json
from compliance_verification.output.compliance_output_creator import create_compliant_json_activity, \
    create_compliance_check_output


def convert_threshold_to_title(threshold):
    return threshold.replace(".", "_") + "_"


def setup_environment():
    # Load environment variables from the .env file
    load_dotenv()
    config_file_path = os.environ['CONFIG_FILE_PATH']
    with open(config_file_path) as f:
        config = json.load(f)
    return config, os.environ['HOME_PATH'], os.environ['THRESHOLD_A'], os.environ['THRESHOLD_R_A']


"""
Pre-Process
    # 1.1 Pre-Process a Description
    # 1.1.1 Using GPT-4
"""


# Step 1 in Process Model
def pre_process_description(home_path, config):
    gpt4_output_path = home_path + config['gpt_4_output_file']
    # Add pattern:
    patterns = detect_and_add_patterns(gpt4_output_path)
    # Load description pre-process file
    with open(gpt4_output_path) as f:
        gpt4_output_file = json.load(f)
    return gpt4_output_file


# Step 2 in Process Model
def pre_process_event_log(home_path, config):
    input_event_log = home_path + config['input_event_log']
    output_path = home_path + config['step_two_output_path']
    path_preprocessed_event_log = create_event_log_pre_process_json(
        input_event_log,
        config['case_id_column_name'],
        config['activity_column_name'],
        config['timestamp_key_name'],
        config['used_separator'],
        config['event_log_file_name'],
        output_path)
    return path_preprocessed_event_log


# Step 3, 4, 5 in Process Model
def compliance_verification(home_path, config, threshold_a, threshold_r_a):
    path_preprocessed_event_log = home_path + config['path_preprocessed_event_log']
    gpt4_output_file_with_patterns = home_path + config['gpt_4_output_file_with_patterns']
    to_execute = config['to_execute']

    # Step 3: Activity Matching
    if to_execute == 'activity_matching' or to_execute == 'all':
        create_compliant_json_activity(
            path_preprocessed_event_log=path_preprocessed_event_log,
            path_preprocessed_description=gpt4_output_file_with_patterns,
            similarity_measure=config['similarity_measure'],  # Choose either: { "TF-IDF", "BERT", or "SPACY"}
            threshold=float(threshold_a),  # Choose a value between 0 and 1
            output_file_name=convert_threshold_to_title(threshold_a) + config['activity_matching_output_file_name'],
            output_path=home_path + config['step_three_output_path']
        )

    # Step 4 and 5: Compliance output
    if to_execute == 'compliance_check' or to_execute == 'all':
        create_compliance_check_output(
            path_preprocessed_event_log=path_preprocessed_event_log,
            path_preprocessed_description=gpt4_output_file_with_patterns,
            similarity_measure=config['similarity_measure'],  # Choose either: { "TF-IDF", "BERT", or "SPACY"}
            threshold=float(threshold_r_a),  # Choose a value between 0 and 1
            resource_types_to_be_checked=config['resource_types'],
            # Choose either: { "['user']", "['role']", "['org_unit']", "['org']", "['user', 'role']", "['user', 'role', 'org_unit', 'org']"}
            check_resource_and_activity=config['check_resource_and_activity'],
            # Choose either True or False: Default False: Only Resource are checked in Step 4
            perform_pattern_rar_check=config['perform_pattern_rar_check'],
            # If True a pattern check is executed, Else default resource compliance check is executed
            file_name=convert_threshold_to_title(threshold_r_a) + config['compliance_check_output_file_name'],  #
            output_path=home_path + config['step_four_five_output_path']
        )


# Execution
def main():
    config, home_path, threshold_a, threshold_r_a = setup_environment()
    if config['to_execute'] == 'all':
        pre_process_description(home_path, config)
        print("Pre-Processed Description successfully done!")
        pre_process_event_log(home_path, config)
        print("Pre-Processed Log successfully done!")

    if config['to_execute'] == 'add_patterns_to_gpt_4_output':
        pre_process_description(home_path, config)
        print("Pre-Processed Description successfully done!")
        exit()

    if config['to_execute'] == 'pre_process_event_log':
        pre_process_event_log(home_path, config)
        print("Pre-Processed Log successfully done!")
        exit()
    compliance_verification(home_path, config, threshold_a, threshold_r_a)
    print("Compliance Verification successfully done!")


if __name__ == "__main__":
    main()
