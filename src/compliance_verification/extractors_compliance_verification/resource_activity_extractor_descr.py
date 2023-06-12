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
from typing import Any
import json


# Resource,Activity can only be used for json of GPT output description
def create_resource_descr_activity_tuples_dict(path_preprocessed_description: str,
                                               activities_description_matched: list[str],
                                               id_matched_description: list[int],
                                               check_res_and_act: bool
                                               ):
    # Store dict with {id: (resource,activity_check_one)}
    resource_activity_dict = __create_pairs_from_descr_activity_list(path_preprocessed_description=path_preprocessed_description,
                                                                     activities_description_matched=activities_description_matched,
                                                                     id_matched_description=id_matched_description,
                                                                     resource_type="resource",
                                                                     check_res_and_act=check_res_and_act
                                                                     )
    return resource_activity_dict


# Helper create specific Resource, Activity pairs:
# Helper only for json of GPT output description
def __create_pairs_from_descr_activity_list(path_preprocessed_description: str,
                                            activities_description_matched: list[str],
                                            id_matched_description: list[int],
                                            resource_type: str,
                                            check_res_and_act: bool
                                            ):
    # Output
    output_list = []

    # Get json file
    with open(path_preprocessed_description) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs_description = json_data["pairs"]

    # Go through the refined activity list
    for i in range(0, len(activities_description_matched)):
        activity = activities_description_matched[i]
        id_description = id_matched_description[i]
        # Check if activity == ""
        if activity == "":
            if check_res_and_act:
                # Resource, Activity Pair
                output_list.append(("", ""))
            else:
                # Resource
                output_list.append("")
        else:
            # Iterate through the pre-processed log and find resource:
            for pair in pairs_description:
                if pair["id"] == id_description:
                    if check_res_and_act:
                        # Resource, Activity Pair
                        output_list.append((pair[resource_type], activity))
                    else:
                        # Resource
                        output_list.append(pair[resource_type])
                    break

    # Return a list that either contains the resources, that need to be checked
    # or the (resource,activity) tuples that need to be checked
    return output_list


# NOT IN USE
def __get_patterns_descr_json(path: str) -> dict[Any, Any]:
    # Store dict with {id: (resource,activity_check_one)}
    resource_pattern_dict = {}
    # Get json file
    with open(path) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs = json_data["pairs"]

    # Iterate through the list
    for distinct_event in pairs:
        # Id (counting)
        id = distinct_event["id"]
        # Resource
        pattern = distinct_event["pattern"]
        resource_pattern_dict[id] = pattern
    # Return dict {id: activity_check_one}
    return resource_pattern_dict
