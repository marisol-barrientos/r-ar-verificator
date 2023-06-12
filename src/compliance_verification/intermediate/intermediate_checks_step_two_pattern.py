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
Perform a Pattern-based Compliance Verification and return the Compliance Outputs
"""

import json


# Check Pattern methods:
def pattern_based_rar_refinement(path_preprocessed_log: str,
                                 ids_of_log: list,
                                 ids_of_description: list,
                                 pattern_list: list,
                                 activity_checks: list,
                                 resources_checked_log: list,
                                 resources_checked_description: list,
                                 resources_similarity_scores: list,
                                 threshold_resource_check: float
                                 ):
    # Compliant list.
    compliant_output = []

    # 1.1 Load json of pre-processed log:
    # Get Json
    with open(path_preprocessed_log) as json_file:
        pre_processed_description_pair = json.load(json_file)
    # Get pre-processed log data
    pre_processed_log_data = pre_processed_description_pair["pairs"]

    # 1.2. Remove the not matched activity pairs from the pattern
    # Remove at same index values in resource_checked_log, resource_checked_description, pattern_list
    i_activity_check = 0
    for matched_activity in activity_checks:
        if matched_activity == '':
            resources_checked_log[i_activity_check] = ''
            resources_checked_description[i_activity_check] = ''
            pattern_list[i_activity_check] = ''
        i_activity_check = i_activity_check + 1

    # 2. Perform pattern-based compliance check
    i_resource_check = 0
    id_output = 1
    for pattern_of_matched_activity in pattern_list:

        # 2.1 Scenario pattern is empty string -> Activity could not be matched
        if pattern_of_matched_activity == '':

            # Non-Compliant: No matched Activity:
            # Complaint output value:
            compliant_output_value = __compliant_output_no_activity_match(id=id_output,
                                                                          id_log=ids_of_log[i_resource_check],
                                                                          id_descr=ids_of_description[i_resource_check],
                                                                          compliant=False,
                                                                          reason='Activity does not exit in Description'
                                                                          )
            # Add value to output list
            compliant_output.append(compliant_output_value)

        # 2.2 Scenario pattern-resource-activity was already checked
        # because of referenced pattern-resource-activity:
        elif pattern_of_matched_activity == 'checked':
            continue

        # 2.3 Scenario: PerformBy or Automatic Pattern:
        elif pattern_of_matched_activity['pattern_id'] == 1 or pattern_of_matched_activity['pattern_id'] == 9:

            # Pattern Check:
            compliant_output_value = __performed_by_automatic_pattern(id=id_output,
                                                                      resource_sim_score=resources_similarity_scores[
                                                                          i_resource_check],
                                                                      threshold_resource_check=threshold_resource_check,
                                                                      pre_processed_log_data=pre_processed_log_data,
                                                                      id_log=ids_of_log[i_resource_check],
                                                                      id_descr=ids_of_description[i_resource_check],
                                                                      matched_activity=activity_checks[
                                                                          i_resource_check],
                                                                      resource_log=resources_checked_log[
                                                                          i_resource_check],
                                                                      resource_descr=resources_checked_description[
                                                                          i_resource_check],
                                                                      pattern=str(pattern_of_matched_activity[
                                                                                      'pattern_id']) + " " + "Performed By / Automatic"
                                                                      )
            # Add to output list:
            compliant_output.append(compliant_output_value)

        # 2.4 Scenario: NotPerformBy  Pattern:
        elif pattern_of_matched_activity['pattern_id'] == 2:

            # Pattern Check:
            compliant_output_value = __not_performed_by_pattern(id=id_output,
                                                                resource_sim_score=resources_similarity_scores[
                                                                    i_resource_check],
                                                                threshold_resource_check=threshold_resource_check,
                                                                pre_processed_log_data=pre_processed_log_data,
                                                                id_log=ids_of_log[i_resource_check],
                                                                id_descr=ids_of_description[i_resource_check],
                                                                matched_activity=activity_checks[
                                                                    i_resource_check],
                                                                resource_log=resources_checked_log[
                                                                    i_resource_check],
                                                                resource_descr=resources_checked_description[
                                                                    i_resource_check],
                                                                pattern=str(pattern_of_matched_activity[
                                                                                'pattern_id']) + " " + "Not Performed By"
                                                                )
            # Add to output list:
            compliant_output.append(compliant_output_value)

        # 2.5 Scenario: Special Pattern 3-8 are detected and checked:
        else:

            # Pattern 3: Dynamic SoD:
            if pattern_of_matched_activity['pattern_id'] == 3:

                # Pattern Check
                compliant_output_dynamic_sod, new_pattern_list = __dynamic_sod_pattern(id=id_output,
                                                                                       resource_sim_score=
                                                                                       resources_similarity_scores[
                                                                                           i_resource_check],
                                                                                       resource_sim_score_list=resources_similarity_scores,
                                                                                       threshold_resource_check=threshold_resource_check,
                                                                                       pre_processed_log_data=pre_processed_log_data,
                                                                                       pattern_of_matched_activity=pattern_of_matched_activity,
                                                                                       id_log_list=ids_of_log,
                                                                                       id_descr_list=ids_of_description,
                                                                                       id_log=ids_of_log[
                                                                                           i_resource_check],
                                                                                       id_descr=ids_of_description[
                                                                                           i_resource_check],
                                                                                       matched_activity=activity_checks[
                                                                                           i_resource_check],
                                                                                       activity_checks=activity_checks,
                                                                                       resource_log=
                                                                                       resources_checked_log[
                                                                                           i_resource_check],
                                                                                       resource_log_list=resources_checked_log,
                                                                                       resource_descr=
                                                                                       resources_checked_description[
                                                                                           i_resource_check],
                                                                                       resource_descr_list=resources_checked_description,
                                                                                       pattern=str(
                                                                                           pattern_of_matched_activity[
                                                                                               'pattern_id']) + " " + "Dynamic SoD",
                                                                                       pattern_list=pattern_list
                                                                                       )
                # New pattern list, maybe checked ones of pattern 3
                pattern_list = new_pattern_list
                # Add compliant values to output list
                for c in compliant_output_dynamic_sod:
                    compliant_output.append(c)

            # Pattern 4: Static SoD or Pattern 6: Dynamic Bonded
            elif pattern_of_matched_activity['pattern_id'] == [4, 6]:

                # Pattern Check
                compliant_output_dynamic_sod, new_pattern_list = __static_sod_pattern(id=id_output,
                                                                                      resource_sim_score=
                                                                                      resources_similarity_scores[
                                                                                          i_resource_check],
                                                                                      resource_sim_score_list=resources_similarity_scores,
                                                                                      threshold_resource_check=threshold_resource_check,
                                                                                      pre_processed_log_data=pre_processed_log_data,
                                                                                      pattern_of_matched_activity=pattern_of_matched_activity,
                                                                                      id_log_list=ids_of_log,
                                                                                      id_descr_list=ids_of_description,
                                                                                      id_log=ids_of_log[
                                                                                          i_resource_check],
                                                                                      id_descr=ids_of_description[
                                                                                          i_resource_check],
                                                                                      matched_activity=activity_checks[
                                                                                          i_resource_check],
                                                                                      activity_checks=activity_checks,
                                                                                      resource_log=
                                                                                      resources_checked_log[
                                                                                          i_resource_check],
                                                                                      resource_log_list=resources_checked_log,
                                                                                      resource_descr=
                                                                                      resources_checked_description[
                                                                                          i_resource_check],
                                                                                      resource_descr_list=resources_checked_description,
                                                                                      pattern=str(
                                                                                          pattern_of_matched_activity[
                                                                                              'pattern_id']) + " " + "Static SoD",
                                                                                      pattern_list=pattern_list
                                                                                      )
                # New pattern list, maybe checked ones of pattern 3
                pattern_list = new_pattern_list
                # Add compliant values to output list
                for c in compliant_output_dynamic_sod:
                    compliant_output.append(c)

            # Pattern 5: Multi-Segregated:
            # elif pattern_of_matched_activity['pattern_id'] == 5:

            # Pattern 6: Dynamic Bonded:
            # elif pattern_of_matched_activity['pattern_id'] == 6:

            # Pattern 7: Static Bonded:
            elif pattern_of_matched_activity['pattern_id'] == 7:

                # Pattern Check
                compliant_output_dynamic_sod, new_pattern_list = __static_bonded_pattern(id=id_output,
                                                                                         resource_sim_score=
                                                                                         resources_similarity_scores[
                                                                                             i_resource_check],
                                                                                         resource_sim_score_list=resources_similarity_scores,
                                                                                         threshold_resource_check=threshold_resource_check,
                                                                                         pre_processed_log_data=pre_processed_log_data,
                                                                                         pattern_of_matched_activity=pattern_of_matched_activity,
                                                                                         id_log_list=ids_of_log,
                                                                                         id_descr_list=ids_of_description,
                                                                                         id_log=ids_of_log[
                                                                                             i_resource_check],
                                                                                         id_descr=ids_of_description[
                                                                                             i_resource_check],
                                                                                         matched_activity=
                                                                                         activity_checks[
                                                                                             i_resource_check],
                                                                                         activity_checks=activity_checks,
                                                                                         resource_log=
                                                                                         resources_checked_log[
                                                                                             i_resource_check],
                                                                                         resource_log_list=resources_checked_log,
                                                                                         resource_descr=
                                                                                         resources_checked_description[
                                                                                             i_resource_check],
                                                                                         resource_descr_list=resources_checked_description,
                                                                                         pattern=str(
                                                                                             pattern_of_matched_activity[
                                                                                                 'pattern_id']) + " " + "Static Bonded",
                                                                                         pattern_list=pattern_list
                                                                                         )
                # New pattern list, maybe checked ones of pattern 3
                pattern_list = new_pattern_list
                # Add compliant values to output list
                for c in compliant_output_dynamic_sod:
                    compliant_output.append(c)

            # Pattern 8: Multi Bonded:
            # elif pattern_of_matched_activity['pattern_id'] == 8:

            # Use always Perform by as long as not all patterns are implemented:
            else:
                # Pattern Check:
                compliant_output_value = __performed_by_automatic_pattern(id=id_output,
                                                                          resource_sim_score=
                                                                          resources_similarity_scores[
                                                                              i_resource_check],
                                                                          threshold_resource_check=threshold_resource_check,
                                                                          pre_processed_log_data=pre_processed_log_data,
                                                                          id_log=ids_of_log[i_resource_check],
                                                                          id_descr=ids_of_description[i_resource_check],
                                                                          matched_activity=activity_checks[
                                                                              i_resource_check],
                                                                          resource_log=resources_checked_log[
                                                                              i_resource_check],
                                                                          resource_descr=resources_checked_description[
                                                                              i_resource_check],
                                                                          pattern=str(pattern_of_matched_activity[
                                                                                          'pattern_id']) + " " + "Performed By / Automatic"
                                                                          )
                # Add to output list:
                compliant_output.append(compliant_output_value)

        # Increment index counter:
        i_resource_check = i_resource_check + 1
        # Increment output id
        id_output = id_output + 1

    return compliant_output


# Modularization: Every Pattern will be implemented in own class and at the end connected in the above main method:

# 1) Performed By/ 9) Automatic:
def __performed_by_automatic_pattern(id: int,
                                     resource_sim_score: float,
                                     threshold_resource_check: float,
                                     pre_processed_log_data: list,
                                     id_log: int,
                                     id_descr: int,
                                     matched_activity: str,
                                     resource_log: str,
                                     resource_descr: str,
                                     pattern: str
                                     ) -> dict:
    # Check if Compliant
    if resource_sim_score >= threshold_resource_check:

        # Compliant:
        # Get traces of compliant pattern result
        traces = __get_traces(pre_processed_log=pre_processed_log_data, id_log=id_log)

        # Compliant output value:
        compliant_output_value = __compliant_output_general(id=id,
                                                            matched_activity=matched_activity,
                                                            resource_log=resource_log,
                                                            resource_descr=resource_descr,
                                                            id_log=id_log,
                                                            id_descr=id_descr,
                                                            sim_score=resource_sim_score,
                                                            traces=traces,
                                                            pattern=pattern,
                                                            compliant=True,
                                                            reason=""
                                                            )

    else:

        # Non-Compliant
        # Get traces of compliant pattern result
        traces = __get_traces(pre_processed_log=pre_processed_log_data, id_log=id_log)

        # Compliant output value:
        compliant_output_value = __compliant_output_general(id=id,
                                                            matched_activity=matched_activity,
                                                            resource_log=resource_log,
                                                            resource_descr=resource_descr,
                                                            id_log=id_log,
                                                            id_descr=id_descr,
                                                            sim_score=resource_sim_score,
                                                            traces=traces,
                                                            pattern=pattern,
                                                            compliant=False,
                                                            reason='Resource-Activity pair not valid'
                                                            )

    return compliant_output_value


# 2) Not Performed By
def __not_performed_by_pattern(id: int,
                               resource_sim_score: float,
                               threshold_resource_check: float,
                               pre_processed_log_data: list,
                               id_log: int,
                               id_descr: int,
                               matched_activity: str,
                               resource_log: str,
                               resource_descr: str,
                               pattern: str
                               ) -> dict:
    # Check if Compliant
    if resource_sim_score < threshold_resource_check:

        # Compliant:
        # Get traces of compliant pattern result
        traces = __get_traces(pre_processed_log=pre_processed_log_data, id_log=id_log)

        # Compliant output value:
        compliant_output_value = __compliant_output_general(id=id,
                                                            matched_activity=matched_activity,
                                                            resource_log=resource_log,
                                                            resource_descr=resource_descr,
                                                            id_log=id_log,
                                                            id_descr=id_descr,
                                                            sim_score=resource_sim_score,
                                                            traces=traces,
                                                            pattern=pattern,
                                                            compliant=True,
                                                            reason=""
                                                            )

    else:

        # Non-Compliant
        # Get traces of compliant pattern result
        traces = __get_traces(pre_processed_log=pre_processed_log_data, id_log=id_log)

        # Compliant output value:
        compliant_output_value = __compliant_output_general(id=id,
                                                            matched_activity=matched_activity,
                                                            resource_log=resource_log,
                                                            resource_descr=resource_descr,
                                                            id_log=id_log,
                                                            id_descr=id_descr,
                                                            sim_score=resource_sim_score,
                                                            traces=traces,
                                                            pattern=pattern,
                                                            compliant=False,
                                                            reason='Resource-Activity pair not valid'
                                                            )

    return compliant_output_value


# 3) Dynamic Sod
def __dynamic_sod_pattern(id: int,
                          resource_sim_score: float,
                          resource_sim_score_list: list,
                          threshold_resource_check: float,
                          pre_processed_log_data: list,
                          pattern_of_matched_activity: dict,
                          id_log_list: list,
                          id_descr_list: list,
                          id_log: int,
                          id_descr: int,
                          matched_activity: str,
                          activity_checks: list,
                          resource_log: str,
                          resource_log_list: list,
                          resource_descr: str,
                          resource_descr_list: list,
                          pattern: str,
                          pattern_list: list
                          ):
    # List of compliant output values of Dynamic SoD:
    compliant_outputs = []

    # 3.1 Get both connected activities:
    # Get current description id and current activity
    current_description_activity = matched_activity

    # Get referenced description id and referenced matched activity
    referenced_description_id = pattern_of_matched_activity['ref_id']
    referenced_description_activity = pattern_of_matched_activity['ref_activity']

    # Get index of referenced id and activity of corresponding lists: ids_of_description and activity_checks
    i_ref = 0
    index_of_corresponding_ra = 0
    for desc_id in id_descr_list:
        if desc_id == referenced_description_id and activity_checks[i_ref]:
            index_of_corresponding_ra = i_ref
            break
        i_ref = i_ref + 1

    # 3.2 Check if activities occur more than once respectively:
    # If yes, eliminated the non-compliant ones:
    i_duplicate_check = 0
    current_res_activities = []
    referenced_res_activities = []
    for activity in activity_checks:

        # Get the infos for the current checked activity
        if activity == current_description_activity:
            current_res_activities.append({'index': i_duplicate_check,
                                           'activity': activity,
                                           'resource_log': resource_log_list[i_duplicate_check],
                                           'resource_descr': resource_descr_list[
                                               i_duplicate_check],
                                           'similarity': resource_sim_score_list[i_duplicate_check]
                                           })
        if activity == referenced_description_activity:
            referenced_res_activities.append({'index': i_duplicate_check,
                                              'activity': activity,
                                              'resource_log': resource_log_list[i_duplicate_check],
                                              'resource_descr': resource_descr_list[
                                                  i_duplicate_check],
                                              'similarity': resource_sim_score_list[i_duplicate_check]
                                              })
        i_duplicate_check = i_duplicate_check + 1

    # EXACTLY ONE activity exist for current and referenced
    if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

        # 3.3 Check if pattern compliant or not:
        # Compliant check for Dynamic SoD
        if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                current_res_activities[0]['resource_log'] != referenced_res_activities[0]['resource_log']:

            # Compliant:
            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check traces:
            traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                traces_cur=traces_cur,
                traces_ref=traces_ref)

            # Check for current activity
            # Check if all traces occur in cur and ref -> wrong is empty
            if not traces_cur_wrong:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

            else:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )
                # Add non-compliant current activity
                compliant_outputs.append(compliant_output_value)

            if not traces_ref_wrong:
                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

            else:

                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

                # Non-Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )

                compliant_outputs.append(compliant_output_value)

            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

        # Dynamic SoD condition not fulfilled -> non-compliant:
        else:

            # Non-Compliant:

            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check if different cases occur for current res act pair or ref res act pair
            # for trace in traces_cur:
            # Compliant current res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=matched_activity,
                                                                resource_log=resource_log,
                                                                resource_descr=resource_descr,
                                                                id_log=id_log,
                                                                id_descr=id_descr,
                                                                sim_score=resource_sim_score,
                                                                traces=traces_cur,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Dynamic SoD Violation"
                                                                )

            # Add compliant current activity
            compliant_outputs.append(compliant_output_value)

            # Compliant referenced res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=activity_checks[
                                                                    index_of_corresponding_ra],
                                                                resource_log=resource_log_list[
                                                                    index_of_corresponding_ra],
                                                                resource_descr=resource_descr_list[
                                                                    index_of_corresponding_ra],
                                                                id_log=id_log_list[index_of_corresponding_ra],
                                                                id_descr=id_descr_list[index_of_corresponding_ra],
                                                                sim_score=resource_sim_score_list[
                                                                    index_of_corresponding_ra],
                                                                traces=traces_ref,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Dynamic SoD Violation"
                                                                )

            # Add compliant referenced activity
            compliant_outputs.append(compliant_output_value)
            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

    # MORE THAN ONE Activity exist
    elif len(current_res_activities) > 1 and len(referenced_res_activities) > 1:

        # The current activity occurs more often in the log:
        if len(current_res_activities) > 1:

            # Check which ones are non-compliant and add them as non-compliant
            for ra_pair in current_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Dynamic SoD Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra pair from list
                    current_res_activities.remove(ra_pair)

        # referenced contains more:
        if len(referenced_res_activities) > 1:

            for ra_pair in referenced_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Dynamic SoD Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra_pair from
                    referenced_res_activities.remove(ra_pair)

        # Check now if after reducing the duplicates form the list if exactly one pair exists
        if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

            # 3.3 Check if pattern compliant or not:
            if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                    referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                    current_res_activities[0]['resource_log'] != referenced_res_activities[0]['resource_log']:

                # Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check traces:
                traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                    traces_cur=traces_cur,
                    traces_ref=traces_ref)

                # Check for current activity
                # Check if all traces occur in cur and ref -> wrong is empty
                if not traces_cur_wrong:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                else:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )
                    # Add non-compliant current activity
                    compliant_outputs.append(compliant_output_value)

                if not traces_ref_wrong:
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                else:

                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

                # Dynamic SoD condition not fulfilled -> non-compliant:
            else:

                # Non-Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check if different cases occur for current res act pair or ref res act pair
                # for trace in traces_cur:
                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Dynamic SoD Violation"
                                                                    )

                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Dynamic SoD Violation"
                                                                    )

                # Add compliant referenced activity
                compliant_outputs.append(compliant_output_value)
                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

    # List of current or referenced activity empty:
    else:
        raise ValueError(
            "Dynamic SoD can not be evaluated since no current or no referenced resource-activity pair exist.")

    return compliant_outputs, pattern_list


# 4) Static SoD
def __static_sod_pattern(id: int,
                         resource_sim_score: float,
                         resource_sim_score_list: list,
                         threshold_resource_check: float,
                         pre_processed_log_data: list,
                         pattern_of_matched_activity: dict,
                         id_log_list: list,
                         id_descr_list: list,
                         id_log: int,
                         id_descr: int,
                         matched_activity: str,
                         activity_checks: list,
                         resource_log: str,
                         resource_log_list: list,
                         resource_descr: str,
                         resource_descr_list: list,
                         pattern: str,
                         pattern_list: list
                         ):
    # List of compliant output values of Dynamic SoD:
    compliant_outputs = []

    # 3.1 Get both connected activities:
    # Get current description id and current activity
    current_description_activity = matched_activity

    # Get referenced description id and referenced matched activity
    referenced_description_id = pattern_of_matched_activity['ref_id']
    referenced_description_activity = pattern_of_matched_activity['ref_activity']

    # Get index of referenced id and activity of corresponding lists: ids_of_description and activity_checks
    i_ref = 0
    index_of_corresponding_ra = 0
    for desc_id in id_descr_list:
        if desc_id == referenced_description_id and activity_checks[i_ref]:
            index_of_corresponding_ra = i_ref
            break
        i_ref = i_ref + 1

    # 3.2 Check if activities occur more than once respectively:
    # If yes, eliminated the non-compliant ones:
    i_duplicate_check = 0
    current_res_activities = []
    referenced_res_activities = []
    for activity in activity_checks:

        # Get the infos for the current checked activity
        if activity == current_description_activity:
            current_res_activities.append({'index': i_duplicate_check,
                                           'activity': activity,
                                           'resource_log': resource_log_list[i_duplicate_check],
                                           'resource_descr': resource_descr_list[
                                               i_duplicate_check],
                                           'similarity': resource_sim_score_list[i_duplicate_check]
                                           })
        if activity == referenced_description_activity:
            referenced_res_activities.append({'index': i_duplicate_check,
                                              'activity': activity,
                                              'resource_log': resource_log_list[i_duplicate_check],
                                              'resource_descr': resource_descr_list[
                                                  i_duplicate_check],
                                              'similarity': resource_sim_score_list[i_duplicate_check]
                                              })
        i_duplicate_check = i_duplicate_check + 1

    # EXACTLY ONE activity exist for current and referenced
    if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

        # 3.3 Check if pattern compliant or not:
        # Compliant check for Static SoD
        if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                current_res_activities[0]['resource_log'] != referenced_res_activities[0]['resource_log'] and \
                current_res_activities[0]['role'] != referenced_res_activities[0]['role']:

            # Compliant:
            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check traces:
            traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                traces_cur=traces_cur,
                traces_ref=traces_ref)

            # Check for current activity
            # Check if all traces occur in cur and ref -> wrong is empty
            if not traces_cur_wrong:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

            else:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )
                # Add non-compliant current activity
                compliant_outputs.append(compliant_output_value)

            if not traces_ref_wrong:
                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

            else:

                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

                # Non-Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )

                compliant_outputs.append(compliant_output_value)

            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

        # Dynamic SoD condition not fulfilled -> non-compliant:
        else:

            # Non-Compliant:

            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check if different cases occur for current res act pair or ref res act pair
            # for trace in traces_cur:
            # Compliant current res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=matched_activity,
                                                                resource_log=resource_log,
                                                                resource_descr=resource_descr,
                                                                id_log=id_log,
                                                                id_descr=id_descr,
                                                                sim_score=resource_sim_score,
                                                                traces=traces_cur,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Static SoD Violation"
                                                                )

            # Add compliant current activity
            compliant_outputs.append(compliant_output_value)

            # Compliant referenced res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=activity_checks[
                                                                    index_of_corresponding_ra],
                                                                resource_log=resource_log_list[
                                                                    index_of_corresponding_ra],
                                                                resource_descr=resource_descr_list[
                                                                    index_of_corresponding_ra],
                                                                id_log=id_log_list[index_of_corresponding_ra],
                                                                id_descr=id_descr_list[index_of_corresponding_ra],
                                                                sim_score=resource_sim_score_list[
                                                                    index_of_corresponding_ra],
                                                                traces=traces_ref,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Static SoD Violation"
                                                                )

            # Add compliant referenced activity
            compliant_outputs.append(compliant_output_value)
            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

    # MORE THAN ONE Activity exist
    elif len(current_res_activities) > 1 and len(referenced_res_activities) > 1:

        # The current activity occurs more often in the log:
        if len(current_res_activities) > 1:

            # Check which ones are non-compliant and add them as non-compliant
            for ra_pair in current_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Static SoD Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra pair from list
                    current_res_activities.remove(ra_pair)

        # referenced contains more:
        if len(referenced_res_activities) > 1:

            for ra_pair in referenced_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Static SoD Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra_pair from
                    referenced_res_activities.remove(ra_pair)

        # Check now if after reducing the duplicates form the list if exactly one pair exists
        if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

            # Static SoD compliant check
            if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                    referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                    current_res_activities[0]['resource_log'] != referenced_res_activities[0]['resource_log'] and \
                    current_res_activities[0]['role'] != referenced_res_activities[0]['role']:

                # Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check traces:
                traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                    traces_cur=traces_cur,
                    traces_ref=traces_ref)

                # Check for current activity
                # Check if all traces occur in cur and ref -> wrong is empty
                if not traces_cur_wrong:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                else:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )
                    # Add non-compliant current activity
                    compliant_outputs.append(compliant_output_value)

                if not traces_ref_wrong:
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                else:

                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

            # Dynamic SoD condition not fulfilled -> non-compliant:
            else:

                # Non-Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check if different cases occur for current res act pair or ref res act pair
                # for trace in traces_cur:
                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Static SoD Violation"
                                                                    )

                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Static SoD Violation"
                                                                    )

                # Add compliant referenced activity
                compliant_outputs.append(compliant_output_value)
                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

    # List of current or referenced activity empty:
    else:
        raise ValueError(
            "Static SoD can not be evaluated since no current or no referenced resource-activity pair exist.")

    return compliant_outputs, pattern_list


# 5) Static Bonded
def __static_bonded_pattern(id: int,
                            resource_sim_score: float,
                            resource_sim_score_list: list,
                            threshold_resource_check: float,
                            pre_processed_log_data: list,
                            pattern_of_matched_activity: dict,
                            id_log_list: list,
                            id_descr_list: list,
                            id_log: int,
                            id_descr: int,
                            matched_activity: str,
                            activity_checks: list,
                            resource_log: str,
                            resource_log_list: list,
                            resource_descr: str,
                            resource_descr_list: list,
                            pattern: str,
                            pattern_list: list
                            ):
    # List of compliant output values of Dynamic SoD:
    compliant_outputs = []

    # 3.1 Get both connected activities:
    # Get current description id and current activity
    current_description_activity = matched_activity

    # Get referenced description id and referenced matched activity
    referenced_description_id = pattern_of_matched_activity['ref_id']
    referenced_description_activity = pattern_of_matched_activity['ref_activity']

    # Get index of referenced id and activity of corresponding lists: ids_of_description and activity_checks
    i_ref = 0
    index_of_corresponding_ra = 0
    for desc_id in id_descr_list:
        if desc_id == referenced_description_id and activity_checks[i_ref]:
            index_of_corresponding_ra = i_ref
            break
        i_ref = i_ref + 1

    # 3.2 Check if activities occur more than once respectively:
    # If yes, eliminated the non-compliant ones:
    i_duplicate_check = 0
    current_res_activities = []
    referenced_res_activities = []
    for activity in activity_checks:

        # Get the infos for the current checked activity
        if activity == current_description_activity:
            current_res_activities.append({'index': i_duplicate_check,
                                           'activity': activity,
                                           'resource_log': resource_log_list[i_duplicate_check],
                                           'resource_descr': resource_descr_list[
                                               i_duplicate_check],
                                           'similarity': resource_sim_score_list[i_duplicate_check]
                                           })
        if activity == referenced_description_activity:
            referenced_res_activities.append({'index': i_duplicate_check,
                                              'activity': activity,
                                              'resource_log': resource_log_list[i_duplicate_check],
                                              'resource_descr': resource_descr_list[
                                                  i_duplicate_check],
                                              'similarity': resource_sim_score_list[i_duplicate_check]
                                              })
        i_duplicate_check = i_duplicate_check + 1

    # EXACTLY ONE activity exist for current and referenced
    if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

        # 3.3 Check if pattern compliant or not:
        # Compliant check for Static Bonded
        if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                current_res_activities[0]['resource_log'] == referenced_res_activities[0][
            'resource_log'] and \
                current_res_activities[0]['role'] == referenced_res_activities[0]['role']:

            # Compliant:
            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check traces:
            traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                traces_cur=traces_cur,
                traces_ref=traces_ref)

            # Check for current activity
            # Check if all traces occur in cur and ref -> wrong is empty
            if not traces_cur_wrong:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

            else:
                # Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )
                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )
                # Add non-compliant current activity
                compliant_outputs.append(compliant_output_value)

            if not traces_ref_wrong:
                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

            else:

                # Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_right,
                                                                    pattern=pattern,
                                                                    compliant=True,
                                                                    reason=''
                                                                    )

                compliant_outputs.append(compliant_output_value)

                # Non-Compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref_wrong,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                    )

                compliant_outputs.append(compliant_output_value)

            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

        # Dynamic SoD condition not fulfilled -> non-compliant:
        else:

            # Non-Compliant:

            # Get traces of compliant pattern result current
            traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log)
            # Get traces of compliant pattern result current referenced
            traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                      id_log=id_log_list[index_of_corresponding_ra])

            # Check if different cases occur for current res act pair or ref res act pair
            # for trace in traces_cur:
            # Compliant current res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=matched_activity,
                                                                resource_log=resource_log,
                                                                resource_descr=resource_descr,
                                                                id_log=id_log,
                                                                id_descr=id_descr,
                                                                sim_score=resource_sim_score,
                                                                traces=traces_cur,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Static Bonded Violation"
                                                                )

            # Add compliant current activity
            compliant_outputs.append(compliant_output_value)

            # Compliant referenced res act pair:
            compliant_output_value = __compliant_output_general(id=id,
                                                                matched_activity=activity_checks[
                                                                    index_of_corresponding_ra],
                                                                resource_log=resource_log_list[
                                                                    index_of_corresponding_ra],
                                                                resource_descr=resource_descr_list[
                                                                    index_of_corresponding_ra],
                                                                id_log=id_log_list[index_of_corresponding_ra],
                                                                id_descr=id_descr_list[index_of_corresponding_ra],
                                                                sim_score=resource_sim_score_list[
                                                                    index_of_corresponding_ra],
                                                                traces=traces_ref,
                                                                pattern=pattern,
                                                                compliant=False,
                                                                reason="Static Bonded Violation"
                                                                )

            # Add compliant referenced activity
            compliant_outputs.append(compliant_output_value)
            # 3.4 Set referenced pattern to checked
            pattern_list[index_of_corresponding_ra] = 'checked'

    # MORE THAN ONE Activity exist
    elif len(current_res_activities) > 1 and len(referenced_res_activities) > 1:

        # The current activity occurs more often in the log:
        if len(current_res_activities) > 1:

            # Check which ones are non-compliant and add them as non-compliant
            for ra_pair in current_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Static Bonded Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra pair from list
                    current_res_activities.remove(ra_pair)

        # referenced contains more:
        if len(referenced_res_activities) > 1:

            for ra_pair in referenced_res_activities:

                if ra_pair['similarity'] < threshold_resource_check:
                    # Get traces for that activity:
                    traces = pre_processed_log_data[ra_pair['index']]['case_id']

                    # Add element to non-compliant
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=ra_pair['activity'],
                                                                        resource_log=ra_pair['resource_log'],
                                                                        resource_descr=ra_pair['resource_description'],
                                                                        id_log=id_log_list[ra_pair['index']],
                                                                        id_descr=id_descr_list[ra_pair['index']],
                                                                        sim_score=ra_pair['similarity'],
                                                                        traces=traces,
                                                                        pattern="3, 1" + " " + "Dynamic SoD + PerformedBy Automatic",
                                                                        compliant=False,
                                                                        reason='Static Bonded Violation: Was a duplicate for a special pattern and violated the PerformedBy/ Automatic Rule'
                                                                        )

                    # Add compliant referenced activity
                    compliant_outputs.append(compliant_output_value)
                    # 3.4 Set referenced pattern to checked
                    pattern_list[ra_pair['index']] = 'checked'
                    # Remove ra_pair from
                    referenced_res_activities.remove(ra_pair)

        # Check now if after reducing the duplicates form the list if exactly one pair exists
        if len(current_res_activities) == 1 and len(referenced_res_activities) == 1:

            # 3.3 Check if pattern compliant or not:
            if current_res_activities[0]['similarity'] >= threshold_resource_check and \
                    referenced_res_activities[0]['similarity'] >= threshold_resource_check and \
                    current_res_activities[0]['resource_log'] == referenced_res_activities[0][
                'resource_log'] and \
                    current_res_activities[0]['role'] == referenced_res_activities[0]['role']:

                # Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check traces:
                traces_cur_right, traces_cur_wrong, traces_ref_right, traces_ref_wrong = __check_all_traces(
                    traces_cur=traces_cur,
                    traces_ref=traces_ref)

                # Check for current activity
                # Check if all traces occur in cur and ref -> wrong is empty
                if not traces_cur_wrong:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                else:
                    # Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )
                    # Add compliant current activity
                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant current res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=matched_activity,
                                                                        resource_log=resource_log,
                                                                        resource_descr=resource_descr,
                                                                        id_log=id_log,
                                                                        id_descr=id_descr,
                                                                        sim_score=resource_sim_score,
                                                                        traces=traces_cur_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )
                    # Add non-compliant current activity
                    compliant_outputs.append(compliant_output_value)

                if not traces_ref_wrong:
                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                else:

                    # Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_right,
                                                                        pattern=pattern,
                                                                        compliant=True,
                                                                        reason=''
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                    # Non-Compliant referenced res act pair:
                    compliant_output_value = __compliant_output_general(id=id,
                                                                        matched_activity=activity_checks[
                                                                            index_of_corresponding_ra],
                                                                        resource_log=resource_log_list[
                                                                            index_of_corresponding_ra],
                                                                        resource_descr=resource_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        id_log=id_log_list[index_of_corresponding_ra],
                                                                        id_descr=id_descr_list[
                                                                            index_of_corresponding_ra],
                                                                        sim_score=resource_sim_score_list[
                                                                            index_of_corresponding_ra],
                                                                        traces=traces_ref_wrong,
                                                                        pattern=pattern,
                                                                        compliant=False,
                                                                        reason="The traces for this resource-activity pair are not part of the other checked activity."
                                                                        )

                    compliant_outputs.append(compliant_output_value)

                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

            # Dynamic SoD condition not fulfilled -> non-compliant:
            else:

                # Non-Compliant:
                # Get traces of compliant pattern result current
                traces_cur = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log)
                # Get traces of compliant pattern result current referenced
                traces_ref = __get_traces(pre_processed_log=pre_processed_log_data,
                                          id_log=id_log_list[index_of_corresponding_ra])

                # Check if different cases occur for current res act pair or ref res act pair
                # for trace in traces_cur:
                # Non-Compliant current res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=matched_activity,
                                                                    resource_log=resource_log,
                                                                    resource_descr=resource_descr,
                                                                    id_log=id_log,
                                                                    id_descr=id_descr,
                                                                    sim_score=resource_sim_score,
                                                                    traces=traces_cur,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Static Bonded Violation"
                                                                    )

                # Add compliant current activity
                compliant_outputs.append(compliant_output_value)

                # Non-compliant referenced res act pair:
                compliant_output_value = __compliant_output_general(id=id,
                                                                    matched_activity=activity_checks[
                                                                        index_of_corresponding_ra],
                                                                    resource_log=resource_log_list[
                                                                        index_of_corresponding_ra],
                                                                    resource_descr=resource_descr_list[
                                                                        index_of_corresponding_ra],
                                                                    id_log=id_log_list[index_of_corresponding_ra],
                                                                    id_descr=id_descr_list[index_of_corresponding_ra],
                                                                    sim_score=resource_sim_score_list[
                                                                        index_of_corresponding_ra],
                                                                    traces=traces_ref,
                                                                    pattern=pattern,
                                                                    compliant=False,
                                                                    reason="Static Bonded Violation"
                                                                    )

                # Add compliant referenced activity
                compliant_outputs.append(compliant_output_value)
                # 3.4 Set referenced pattern to checked
                pattern_list[index_of_corresponding_ra] = 'checked'

    # List of current or referenced activity empty:
    else:
        raise ValueError(
            "Static Bonded can not be evaluated since no current or no referenced resource-activity pair exist.")

    return compliant_outputs, pattern_list


# Helper Method:
# Check if both activities occur in the same traces
def __check_all_traces(traces_cur: dict, traces_ref: dict):
    # List of keys
    trace_cur_list = list(traces_cur.keys())
    trace_ref_list = list(traces_ref.keys())

    # Traces that occur in both cases
    trace_cur_list_right = {}
    trace_ref_list_right = {}

    # Trace that is only in cur
    trace_cur_list_errors = {}
    # Trace that is only in ref
    trace_ref_list_errors = {}

    # Check if traces in current do not occur in ref
    for trace_cur in trace_cur_list:
        if trace_cur not in trace_ref_list:
            trace_cur_list_errors[trace_cur] = traces_cur[trace_cur]
        else:
            trace_cur_list_right[trace_cur] = traces_cur[trace_cur]

    # Check if traces in ref do not occur in cur
    for trace_ref in trace_ref_list:
        if trace_ref not in trace_cur_list:
            trace_ref_list_errors[trace_ref] = traces_ref[trace_ref]
        else:
            trace_ref_list_right[trace_ref] = traces_ref[trace_ref]

    # Return all right and error traces in cur and ref respectively
    return trace_cur_list_right, trace_cur_list_errors, trace_ref_list_right, trace_ref_list_errors


# Helper Methods General

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
