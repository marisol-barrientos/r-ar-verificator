"""
In this file all the necessary information is generated based on the matched activities and the corresponding
R-AR Patterns. A List of dictionaries will be returned.
"""

import json


def check_and_return_pattern(pre_processed_description_path: str, matched_description_ids: list[int]):
    # Get Json
    with open(pre_processed_description_path) as json_file:
        pre_processed_description_pair = json.load(json_file)
    # Get pre-processed description data
    pre_processed_description_data = pre_processed_description_pair["pairs"]

    # Get Pattern
    patterns = []
    for id_description in matched_description_ids:
        for pre_processed_description_value in pre_processed_description_data:
            if pre_processed_description_value["id"] == id_description:

                if type(pre_processed_description_value["pattern"]["id"]) is not list:

                    # 1: Performed by:
                    # Returns pattern_id
                    if pre_processed_description_value["pattern"]["id"] == 1:
                        patterns.append({"pattern_id": 1, "role_res": None,
                                         "ref_id": None, "ref_resource": None, "ref_activity": None, "ref_role": None,
                                         "min": None, "max": None, "equal": None})

                    # 2: Not Performed by:
                    # Returns pattern_id
                    if pre_processed_description_value["pattern"]["id"] == 2:
                        patterns.append({"pattern_id": 2, "role_res": None,
                                         "ref_id": None, "ref_resource": None, "ref_activity": None, "ref_role": None,
                                         "min": None, "max": None, "equal": None})

                    # 3. Dynamic SoD
                    # Returns pattern_id, referenced id in exclusion, referenced resource and referenced activity
                    if pre_processed_description_value["pattern"]["id"] == 3:
                        ref_id = pre_processed_description_value["exclusion"][0]
                        ref_resource = ""
                        ref_activity = ""
                        for pre_processed_description_value3 in pre_processed_description_data:
                            if pre_processed_description_value3["id"] == ref_id:
                                ref_resource = pre_processed_description_value3["resource"]
                                ref_activity = pre_processed_description_value3["activity"]
                        patterns.append(
                            {"pattern_id": 3, "role_res": None,
                             "ref_id": ref_id, "ref_resource": ref_resource, "ref_activity": ref_activity, "ref_role": None,
                             "min": None, "max": None, "equal": None})

                    # 5. Multi_Segregated
                    # Returns pattern_id, min, max and equal
                    if pre_processed_description_value["pattern"]["id"] == 5:
                        min_d = pre_processed_description_value["min"]
                        max_d = pre_processed_description_value["max"]
                        equal_d = pre_processed_description_value["equals"]
                        patterns.append({"pattern_id": 5, "role_res": None,
                                         "ref_id": None, "ref_resource": None, "ref_activity": None, "ref_role": None,
                                         "min": min_d, "max": max_d, "equals": equal_d})

                    # 7. Static_Bonded
                    # Returns pattern_id, referenced ids in inclusion, referenced resources and referenced activities
                    if pre_processed_description_value["pattern"]["id"] == 7:
                        ref_ids = pre_processed_description_value["inclusion"]
                        ref_resource = []
                        ref_activity = []
                        for ref_id in ref_ids:
                            for pre_processed_description_value3 in pre_processed_description_data:
                                if pre_processed_description_value3["id"] == ref_id:
                                    ref_resource.append(pre_processed_description_value3["resource"])
                                    ref_activity.append(pre_processed_description_value3["activity"])
                            patterns.append(
                                {"pattern_id": 7, "role_res": None,
                                 "ref_id": ref_ids, "ref_resource": ref_resource, "ref_activity": ref_activity, "ref_role": None,
                                 "min": None, "max": None, "equal": None})

                    # 8. Multi_Bonded
                    # Returns pattern_id, referenced ids in inclusion, referenced resources and referenced activities
                    if pre_processed_description_value["pattern"]["id"] == 8:
                        ref_ids = pre_processed_description_value["inclusion"]
                        ref_resource = []
                        ref_activity = []
                        for ref_id in ref_ids:
                            for pre_processed_description_value3 in pre_processed_description_data:
                                if pre_processed_description_value3["id"] == ref_id:
                                    ref_resource.append(pre_processed_description_value3["resource"])
                                    ref_activity.append(pre_processed_description_value3["activity"])
                            patterns.append(
                                {"pattern_id": 8, "role_res": None,
                                 "ref_id": ref_ids, "ref_resource": ref_resource, "ref_activity": ref_activity, "ref_role": None,
                                 "min": None, "max": None, "equal": None})

                    # 9. Automatic
                    # Returns only pattern id
                    if pre_processed_description_value["pattern"]["id"] == 9:
                        patterns.append({"pattern_id": 9, "role_res": None,
                                         "ref_id": None, "ref_resource": None, "ref_activity": None, "ref_role": None,
                                         "min": None, "max": None, "equal": None})

                else:
                    # 4 Static SoD || 6 Dynamic Bonded:
                    # Returns pattern_ids, role of resource, referenced id in exclusion, referenced resource and referenced activity
                    if (pre_processed_description_value["pattern"]["id"][0] == 4
                            and pre_processed_description_value["pattern"]["id"][1] == 6):
                        ref_id = pre_processed_description_value["exclusion"][0]
                        ref_resource = ""
                        ref_activity = ""
                        ref_role = ""
                        role = pre_processed_description_value["role"]
                        for pre_processed_description_value3 in pre_processed_description_data:
                            if pre_processed_description_value3["id"] == ref_id:
                                ref_resource = pre_processed_description_value3["resource"]
                                ref_activity = pre_processed_description_value3["activity"]
                        patterns.append(
                            {"pattern_id": [4, 6], "role_res": role,
                             "ref_id": ref_id, "ref_resource": ref_resource, "ref_activity": ref_activity, "ref_role": ref_role,
                             "min": None, "max": None, "equal": None})

    # Return the patterns
    return patterns
