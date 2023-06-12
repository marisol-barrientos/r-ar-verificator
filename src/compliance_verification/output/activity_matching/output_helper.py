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
"""

"""
import json
import os


# Similarity Check Output 1
# One json with new activity, old activity, original activity of log, similarity score
def create_compliant_json_activity_helper(path_pre_processed_event_log: str,
                                          path_pre_processed_description: str,
                                          activity_list: dict,
                                          similarity_score_list: list,
                                          measure_types: dict,
                                          output_file_name: str,
                                          output_path: str):
    # List that stores the activity check output
    activity_dict_list = []

    # Get json file of log
    with open(path_pre_processed_event_log) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs = json_data["pairs"]

    # Get json file of log
    with open(path_pre_processed_description) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs_descr = json_data["pairs"]

    i = 0
    id_activity_output = 1
    for distinct_event in pairs:
        description_pair_id = __find_description_pair_id(activity_list[i], pairs_descr, check_type=1)

        activity_dict = {"Id": id_activity_output,
                         "Id_in_Log": distinct_event["id"],
                         "Id_in_Description": description_pair_id,
                         "Activity_in_Log": distinct_event["activity"],
                         "Detected_Activity": activity_list[i],
                         "Similarity_Score": similarity_score_list[i]}
        # Increment Index
        i = i + 1
        id_activity_output = id_activity_output + 1
        # Add dict to list
        activity_dict_list.append(activity_dict)

    output_dict = {"measure_types": measure_types,
                   "activity_matching_output": activity_dict_list}
    # Generate json
    __generate_json_from_dict(output_dict=output_dict, file_name=output_file_name + "_activity_check.json",
                              output_path=output_path)


# Helper Methods
def __generate_json_from_dict(output_dict: dict, file_name: str, output_path: str):
    """
    :param output_dict.
    :type dict

    :param file_name.
    :type str

    :param output_path.
    :type str

    """
    # Output data
    json_output = json.dumps(output_dict, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path + file_name, 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=4, default=str)
    return json_output


def __get_org_structure_output(org_structure_descr: list, org_structure_log: list, res_act: str,
                               description_pair_id: str) -> list:
    """
    Returns the information of type/ structure of the resource is given in the log and,
    whether it is valid or invalid.

    :param org_structure_descr.
    :type list

    :param org_structure_log.
    :type list

    :param res_act.
    :type str

    :param description_pair_id.
    :type str

    :returns A list of strings.
    :rtype list
    """

    if description_pair_id in ["None", ""]:
        return ["activity_not_in_rar_set"]
    labels = ["user", "role", "org_unit", "organization"]
    i = 0
    org_structure_output = []
    for field in org_structure_descr:
        # If there is any information in neither log nor in the description then the field is "okay" (lack of info)
        if org_structure_log[i] == "u" and field[i] in ["not_specified", "any_user", ""]:
            org_structure_output.append(labels[i] + "_ok")

        if org_structure_log[i] != "u" and field[i] not in ["not_specified", "any_user", ""]:
            # if event belong to non-complaints...
            if res_act == "":
                org_structure_output.append(labels[i] + "_not_ok")
            # # if event belong to complaints...
            else:
                org_structure_output.append(labels[i] + "_ok")

        # If there is only info in the log...
        if org_structure_log[i] != "u" and field[i] in ["not_specified", "any_user", ""]:
            org_structure_output.append(labels[i] + "_extra_in_log")

        # If there is only info in the description...
        if org_structure_log[i] == "u" and field[i] not in ["not_specified", "any_user", ""]:
            org_structure_output.append(labels[i] + "_missing_in_log")

        i += 1
    return org_structure_output


def __find_description_pair_id(log_output: str, description_pairs: list, check_type: int) -> str:
    """
    :param log_output.
    :type str

    :param description_pairs.
    :type list

    :returns A String.
    :rtype str
    """

    for pair in description_pairs:
        activity_or_resource_activity_str = ""
        if check_type == 1:
            activity_or_resource_activity_str = pair["activity"]
        if check_type == 2:
            activity_or_resource_activity_str = pair["resource"] + ' ' + pair["activity"]
        if activity_or_resource_activity_str == log_output:
            return pair["id"]
    return 'None'


def __find_description_user_role_org_unit_organization(descr_id: str, description_pairs: list) -> list:
    """
    :param descr_id.
    :type str

    :param description_pairs.
    :type list

    :returns A list.
    :rtype list
    """

    for pair in description_pairs:
        if pair["id"] == descr_id:
            return [pair["user"], pair["role"], pair["org_unit"], pair["organization"]]
    return ['None']
