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
Helper methods, to generate dictionaries where the value is a resource activity tuple list.
"""
from typing import List, Any, Union
import json


# For description and Log usable
# Single:
# User,Activity tuples, can be used for log and description json
def create_user_activity_tuples_list(path_pre_processed_log: str,
                                     refined_activity_list_log: List[str],
                                     id_refined_log: list[int],
                                     check_res_and_act: bool
                                     ) -> list:
    # Store dict with {id: (org_unit, activity_check_one)}
    user_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_single(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_type="user",
        check_res_and_act=check_res_and_act
    )
    return user_activities_list


# Role,Activity tuples, can be used for log and description json
def create_role_activity_tuples_list(path_pre_processed_log: str,
                                     refined_activity_list_log: List[str],
                                     id_refined_log: list[int],
                                     check_res_and_act: bool
                                     ) -> list:
    # Store dict with {id: (role, activity_check_one)}
    role_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_single(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_type="role",
        check_res_and_act=check_res_and_act
    )
    return role_activities_list


# Organizational_Unit,Activity tuples, can be used for log and description json
def create_org_unit_activity_tuples_list(path_pre_processed_log: str,
                                         refined_activity_list_log: List[str],
                                         id_refined_log: list[int],
                                         check_res_and_act: bool
                                         ) -> list:
    org_unit_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_single(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_type="org_unit",
        check_res_and_act=check_res_and_act
    )
    return org_unit_activities_list


# Organization,Activity tuples, can be used for log and description json
def create_org_activity_tuples_list(path_pre_processed_log: str,
                                    refined_activity_list_log: List[str],
                                    id_refined_log: list[int],
                                    check_res_and_act: bool
                                    ) -> list:
    org_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_single(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_type="organization",
        check_res_and_act=check_res_and_act
    )
    return org_activities_list


# Needs tp be refined
# Combinations
# Role,Activity tuples, can be used for log and description json
def create_user_and_role_activity_tuples_list(path_pre_processed_log: str,
                                              refined_activity_list_log: List[str],
                                              id_refined_log: list[int],
                                              check_res_and_act: bool
                                              ) -> list:
    # Store dict with {id: (role, activity_check_one)}
    user_role_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_combi(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_types=['user', 'role'],
        check_res_and_act=check_res_and_act
    )
    return user_role_activities_list


# Organizational_Unit,Activity tuples, can be used for log and description json
def create_role_and_org_unit_activity_tuples_list(path_pre_processed_log: str,
                                                  refined_activity_list_log: List[str],
                                                  id_refined_log: list[int],
                                                  check_res_and_act: bool
                                                  ) -> list:
    # Store dict with {id: (org_unit, activity_check_one)}
    role_org_unit_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_combi(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_types=['role', 'org_unit'],
        check_res_and_act=check_res_and_act
    )
    return role_org_unit_activities_list


# Organizational_Unit,Activity tuples, can be used for log and description json
def create_org_unit_and_org_activity_tuples_list(path_pre_processed_log: str,
                                                 refined_activity_list_log: List[str],
                                                 id_refined_log: list[int],
                                                 check_res_and_act: bool
                                                 ) -> list:
    # Store dict with {id: (org_unit, activity_check_one)}
    org_unit_org_activities_list = __create_resource_or_resource_activity_list_from_pre_processed_log_combi(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_types=['org_unit', 'organization'],
        check_res_and_act=check_res_and_act
    )
    return org_unit_org_activities_list


# Organization,Activity tuples, can be used for log and description json
def create_user_role_org_unit_and_org_activity_tuples_list(path_pre_processed_log: str,
                                                           refined_activity_list_log: List[str],
                                                           id_refined_log: list[int],
                                                           check_res_and_act: bool
                                                           ) -> list:
    # Store dict with {id: (organization,activity_check_one)}
    user_role_org_unit_org_activities_dict = __create_resource_or_resource_activity_list_from_pre_processed_log_combi(
        path_pre_processed_log=path_pre_processed_log,
        refined_activity_list_log=refined_activity_list_log,
        id_refined_log=id_refined_log,
        resource_types=['user', 'role', 'org_unit', 'organization'],
        check_res_and_act=check_res_and_act
    )
    return user_role_org_unit_org_activities_dict


# Single:
# Helper: Create specific Resource, Activity pairs:
def __create_resource_or_resource_activity_list_from_pre_processed_log_single(path_pre_processed_log: str,
                                                                              refined_activity_list_log: list[str],
                                                                              id_refined_log: list[int],
                                                                              resource_type: str,
                                                                              check_res_and_act: bool
                                                                              ) -> list:
    output_list = []

    # Store dict with {id: resource or (resource,activity)}
    resource_activity_dict = {}
    # Get json file
    with open(path_pre_processed_log) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs_log = json_data["pairs"]

    # Go through the refined activity list
    for i in range(0, len(refined_activity_list_log)):
        activity = refined_activity_list_log[i]
        id_log = id_refined_log[i]
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
            for pair in pairs_log:
                if pair["id"] == id_log:
                    # Check resource granularity:
                    resource = __resource_granularity_improvement_single(pre_processed_log_value=pair,
                                                                         resource_type=resource_type)
                    if check_res_and_act:
                        # Resource, Activity Pair
                        output_list.append((resource, activity))
                    else:
                        # Resource
                        output_list.append(resource)
                    break

    # Return a list that either contains the resources, that need to be checked
    # or the (resource,activity) tuples that need to be checked
    return output_list


# Improve the resource granularity in case the chosen resource type is zero
def __resource_granularity_improvement_single(pre_processed_log_value: dict,
                                              resource_type: str
                                              ) -> str:
    resource = ""
    if resource_type == 'org_unit':
        if pre_processed_log_value[resource_type] == 'undefined':
            resource = 'automatic'
        elif pre_processed_log_value[resource_type] == 'u':
            if pre_processed_log_value['user'] != 'u' and pre_processed_log_value['role'] != 'u' and \
                    pre_processed_log_value['organization'] != 'u':
                resource = pre_processed_log_value['user'] + " the " + pre_processed_log_value['role'] + " at " + \
                           pre_processed_log_value['organization']
            elif pre_processed_log_value['user'] != 'u' and pre_processed_log_value['role'] != 'u' and \
                    pre_processed_log_value['organization'] == 'u':
                resource = pre_processed_log_value['user'] + " the " + pre_processed_log_value['role']
            elif pre_processed_log_value['user'] != 'u' and pre_processed_log_value['role'] == 'u' and \
                    pre_processed_log_value['organization'] != 'u' and pre_processed_log_value['organization'] != 'u ':
                resource = pre_processed_log_value['user'] + " at " + pre_processed_log_value['organization']
            elif pre_processed_log_value['user'] == 'u' and pre_processed_log_value['role'] != 'u' and \
                    pre_processed_log_value['organization'] != 'u' and pre_processed_log_value['organization'] != 'u ':
                resource = pre_processed_log_value['role'] + " at " + pre_processed_log_value['organization']
            elif pre_processed_log_value['user'] != 'u' and pre_processed_log_value['role'] == 'u' and \
                    pre_processed_log_value['organization'] == 'u':
                resource = pre_processed_log_value['user']
            elif pre_processed_log_value['user'] == 'u' and pre_processed_log_value['role'] == 'u' and \
                    pre_processed_log_value['organization'] != 'u':
                resource = pre_processed_log_value['organization']
            elif pre_processed_log_value['user'] == 'u' and pre_processed_log_value['role'] != 'u' and \
                    pre_processed_log_value['organization'] == 'u':
                resource = pre_processed_log_value['role']
            elif pre_processed_log_value['user'] == 'u' and pre_processed_log_value['role'] == 'u' and \
                    pre_processed_log_value['organization'] == 'u':
                resource = ""
            else:
                print(pre_processed_log_value)
                raise ValueError("Something went wrong with resource extraction from the pre-processed event log!")
        else:
            resource = pre_processed_log_value[resource_type]

    return resource


# Combi:
# Helper create specific Resource, Activity pairs:
def __create_resource_or_resource_activity_list_from_pre_processed_log_combi(path_pre_processed_log: str,
                                                                             refined_activity_list_log: list[str],
                                                                             id_refined_log: list[int],
                                                                             resource_types: list[str],
                                                                             check_res_and_act: bool
                                                                             ) \
        -> list[Union[Union[tuple[str, str], str, tuple[Union[str, Any], str]], Any]]:
    output_list = []

    # Store dict with {id: resource or (resource,activity)}
    resource_activity_dict = {}
    # Get json file
    with open(path_pre_processed_log) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs_log = json_data["pairs"]

    # Go through the refined activity list
    for i in range(0, len(refined_activity_list_log)):
        activity = refined_activity_list_log[i]
        id_log = id_refined_log[i]
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
            for pair in pairs_log:
                if pair["id"] == id_log:
                    if check_res_and_act:
                        # Resource, Activity Pair
                        # Resource
                        resource = ""
                        for resource_type in resource_types:
                            if pair[resource_type] != "u":
                                resource = resource + " " + pair[resource_type]
                        if check_res_and_act:
                            # Resource, Activity
                            output_list.append((resource, activity))
                        else:
                            # Resource
                            output_list.append(resource)
                    break

    # Return a list that either contains the resources, that need to be checked
    # or the (resource,activity) tuples that need to be checked
    return output_list
