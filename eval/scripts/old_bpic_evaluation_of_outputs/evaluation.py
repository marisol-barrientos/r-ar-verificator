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

# Load environment variables from the .env file
load_dotenv()
HOME_PATH = os.environ['HOME_PATH']

# Used Bert, only role for log pre-process output and resource for description pre-process ouput, threshold activity = 0.8, threshold resource-activity = 0.9

path_compliant = HOME_PATH + "src/evaluate_results/output/compliance_verification_component/bpic/bpic_merged_data_log_event_compliant_output.json"
path_log_output = HOME_PATH + "src/evaluate_results/output/1_step_two/bpic/merged_data.json"

def filter_activities_in_log_output(path_log):
    activity_list = []
    role_list = []

    role_and_activity = []
    with open(path_log) as fp:
        data = json.load(fp)
        pairs = data["pairs"]
    for value in pairs:
        activity_list.append(value["activity"])
        role_list.append(value["role"])

        role_and_activity.append(value["role"] + " " + value["role"])
    return activity_list, role_list, role_and_activity


def filter_ditsinct_event_id_and_description_id(path_compliant_file):
    with open(path_compliant) as fp:
        role_and_activity_compliant_detected = []
        role_and_activity_compliant_log = []

        role_and_activity_non_compliant_detected = []
        role_and_activity_non_compliant_log = []

        data = json.load(fp)
        compliant = data["compliant_output"]
        non_compliant = data["non_compliant_output"]

        for value in compliant:
            role_and_activity_compliant_detected.append(value["resource_activity_detected"])
            role_and_activity_compliant_log.append(value["role_in_log"] + " " + value["activity_in_log"])

        for value in non_compliant:
            role_and_activity_non_compliant_detected.append(value["resource_activity_detected"])
            role_and_activity_non_compliant_log.append(value["role_in_log"] + " " + value["activity_in_log"])
        
        return  role_and_activity_compliant_detected, role_and_activity_compliant_log, role_and_activity_non_compliant_detected, role_and_activity_non_compliant_log
        
            



#activity_list, role_list, role_and  = filter_activities_in_log_output(path_log_output)

#print("")
#print(activity_list)
#print("")
#print(role_list)

role_and_activity_compliant_detected, role_and_activity_compliant_log, role_and_activity_non_compliant_detected, role_and_activity_non_compliant_log = filter_ditsinct_event_id_and_description_id(path_compliant)

print("Compliant:")
for i in range(len(role_and_activity_compliant_detected)):
    print("")
    print("Detected:   " + role_and_activity_compliant_detected[i] + "               " + "Log:   " + role_and_activity_compliant_log[i])

print("")
print(len(role_and_activity_compliant_detected))
print("")

print("Compliant:")
for i in range(len(role_and_activity_non_compliant_detected)):
    print("")
    print("Detected:   " + role_and_activity_non_compliant_detected[i] + "               " + "Log:   " + role_and_activity_non_compliant_log[i])

print("")
print(len(role_and_activity_non_compliant_detected))
print("")


#print("")
#print(role_and_activity_compliant_detected)
#print("")
#print(role_and_activity_compliant_log)
#print("")