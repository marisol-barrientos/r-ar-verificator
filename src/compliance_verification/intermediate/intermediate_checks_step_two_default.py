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
This file creates a list of compliant output dicts for the default pattern based approach.
It distinguishes between Performed By/ Automatic and NotPerformed By.
"""

import json


def default_based_rar_refinement(path_preprocessed_log: str,
                                 ids_of_log: list,
                                 ids_of_description: list,
                                 pattern_list: list[dict],
                                 activity_checks: list,
                                 resources_checked_log: list,
                                 resources_checked_description: list,
                                 resources_similarity_scores: list,
                                 threshold_resource_check: float
                                 ):
    # Compliant list.
    compliant_output = []

    # 1. Load json of pre-processed log:
    # Get Json
    with open(path_preprocessed_log) as json_file:
        pre_processed_description_pair = json.load(json_file)
    # Get pre-processed log data
    pre_processed_log_data = pre_processed_description_pair["pairs"]

    # 2. Remove the not matched activity pairs from the pattern
    # Remove at same index values in resource_checked_log, resource_checked_description, pattern_list
    i_activity_check = 0
    for matched_activity in activity_checks:
        if matched_activity == '':
            resources_checked_log[i_activity_check] = ''
            resources_checked_description[i_activity_check] = ''
        i_activity_check = i_activity_check + 1

    # 3. Perform pattern-based compliance check
    i_resource_check = 0
    id_output = 1
    for activity in activity_checks:

        # 2.1 Scenario pattern is empty string -> Activity could not be matched
        if activity == '':
            # Add non compliant value for no matched activity found reason:
            compliant_value = __compliant_output_no_activity_match(id=id_output,
                                                                   id_log=ids_of_log[i_resource_check],
                                                                   id_descr=ids_of_description[i_resource_check],
                                                                   compliant=False,
                                                                   reason='Activity does not exit in Description')
            compliant_output.append(compliant_value)

        # 2.2 Activity could be matched: Perform similarity check.
        else:
            pattern = pattern_list[i_resource_check]
            # Not Perform By pattern:
            if pattern['pattern_id'] == 2:

                # Similarity must be low -> low resource similarity -> compliant
                if resources_similarity_scores[i_resource_check] < threshold_resource_check:

                    # Get traces of compliant pattern result
                    traces = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=ids_of_log[i_resource_check])

                    compliant_value = __compliant_output_general(id=id_output,
                                                                 matched_activity=activity_checks[i_resource_check],
                                                                 resource_log=resources_checked_log[i_resource_check],
                                                                 resource_descr=resources_checked_description[
                                                                     i_resource_check],
                                                                 id_log=ids_of_log[i_resource_check],
                                                                 id_descr=ids_of_description[i_resource_check],
                                                                 sim_score=resources_similarity_scores[
                                                                     i_resource_check],
                                                                 traces=traces,
                                                                 pattern="2 Not Performed By",
                                                                 compliant=True,
                                                                 reason=""
                                                                 )
                    # Add compliant value to output
                    compliant_output.append(compliant_value)

                else:
                    # Get traces of compliant pattern result
                    traces = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=ids_of_log[i_resource_check])

                    compliant_value = __compliant_output_general(id=id_output,
                                                                 matched_activity=activity_checks[i_resource_check],
                                                                 resource_log=resources_checked_log[i_resource_check],
                                                                 resource_descr=resources_checked_description[
                                                                     i_resource_check],
                                                                 id_log=ids_of_log[i_resource_check],
                                                                 id_descr=ids_of_description[i_resource_check],
                                                                 sim_score=resources_similarity_scores[
                                                                     i_resource_check],
                                                                 traces=traces,
                                                                 pattern="2 Not Performed By",
                                                                 compliant=False,
                                                                 reason='Resource-Activity pair not valid'
                                                                 )
                    # Add compliant value to output
                    compliant_output.append(compliant_value)

            # All other patterns are transformed to perform by:
            else:

                # Similarity score must be high -> high resource similarity -> compliant
                if resources_similarity_scores[i_resource_check] >= threshold_resource_check:

                    # Get traces of compliant pattern result
                    traces = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=ids_of_log[i_resource_check])

                    compliant_value = __compliant_output_general(id=id_output,
                                                                 matched_activity=activity_checks[i_resource_check],
                                                                 resource_log=resources_checked_log[i_resource_check],
                                                                 resource_descr=resources_checked_description[
                                                                     i_resource_check],
                                                                 id_log=ids_of_log[i_resource_check],
                                                                 id_descr=ids_of_description[i_resource_check],
                                                                 sim_score=resources_similarity_scores[
                                                                     i_resource_check],
                                                                 traces=traces,
                                                                 pattern="1 Performed By",
                                                                 compliant=True,
                                                                 reason=""
                                                                 )
                    # Add compliant value to output
                    compliant_output.append(compliant_value)

                else:

                    # Get traces of compliant pattern result
                    traces = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=ids_of_log[i_resource_check])

                    compliant_value = __compliant_output_general(id=id_output,
                                                                 matched_activity=activity_checks[i_resource_check],
                                                                 resource_log=resources_checked_log[i_resource_check],
                                                                 resource_descr=resources_checked_description[
                                                                     i_resource_check],
                                                                 id_log=ids_of_log[i_resource_check],
                                                                 id_descr=ids_of_description[i_resource_check],
                                                                 sim_score=resources_similarity_scores[
                                                                     i_resource_check],
                                                                 traces=traces,
                                                                 pattern="1 Performed By",
                                                                 compliant=False,
                                                                 reason='Resource-Activity pair not valid'
                                                                 )
                    # Add compliant value to output
                    compliant_output.append(compliant_value)

        # Increase index to check the next distinct event
        i_resource_check = i_resource_check + 1
        # Increase output id
        id_output = id_output + 1

    # Compliant and non-compliant documents
    return compliant_output


# Get the traces for the specific id (Index) in the pre-processed event log
def __get_traces(pre_processed_log: list, id_log: int) -> dict:
    # Get traces of non-compliant pattern result
    traces = {}
    for log_value in pre_processed_log:
        if log_value['id'] == id_log:
            traces = log_value['case_id']
            break
    return traces


# Output format for compliance check when activity has no match
def __compliant_output_no_activity_match(id: int, id_log: int, id_descr: int, compliant: bool, reason: str) -> dict:
    return {'Id': id,
            'Id_in_Log': id_log,
            'Id_in_Description': id_descr,
            'Compliant': compliant,
            'Non-Compliant Reason': reason
            }


# Output format for compliance check when either pattern was wrong or resource activity pair is wrong
def __compliant_output_general(id: int, matched_activity: str, resource_log: str, resource_descr: str, id_log: int,
                               id_descr: int, sim_score: float, traces: dict, pattern: str, compliant: bool,
                               reason: str) -> dict:
    return {'Id': id,
            'Matched_activity': matched_activity,
            'Resource_Log': resource_log,
            'Resource_Description': resource_descr,
            'Id_in_Log': id_log,
            'Id_in_Description': id_descr,
            'Similarity_score_of_matched_resources': sim_score,
            'Corresponding traces': traces,
            'Pattern': pattern,
            'Compliant': compliant,
            'Non-Compliant Reason': reason
            }
