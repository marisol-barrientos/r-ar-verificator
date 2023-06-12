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
#
"""
This file implements the process and method flow of the R-AR Verificator V2.
"""

# Required Imports
from typing import Any
#
from ast import literal_eval

from ast import literal_eval

# Similarity Measures
from similarity_measures.similarity_tfidf import activity_similarity_check_one_tfidf, \
    resource_activity_similarity_check_two_tfidf
from similarity_measures.similarity_bert import activity_similarity_check_one_bert, \
    resource_activity_similarity_check_two_bert
from similarity_measures.similarity_spacy import activity_similarity_check_one_spacy, \
    resource_activity_similarity_check_two_spacy

# Pattern Checks
from pattern.pattern_connector import check_and_return_pattern

# 1. Activity Extractor
import extractors_compliance_verification.activities_extractor as act_extractor

# 2. Intermediate cleaner
import intermediate.intermediate_checks_step_one as intermediate_one
import intermediate.intermediate_checks_step_two_default as intermediate_two_default
import intermediate.intermediate_checks_step_two_pattern as intermediate_two_pattern

# 3. Resource Activity Extractor/ Merger
import extractors_compliance_verification.resource_activity_extractor_log as res_act_extractor_log
import extractors_compliance_verification.resource_activity_extractor_descr as res_act_extractor_descr


# Component 1: Executes similarity check for Activities
def resource_activity_compliance_check_step_one(path_preprocessed_event_log: str,
                                                path_preprocessed_description: str,
                                                similarity_measure: str,
                                                threshold: float
                                                ) -> Any:
    # 1. Activity Extraction
    # Get activity dicts for log and description
    dict_activity_log = act_extractor.get_activities_dict_from_json(path_preprocessed_event_log)
    dict_activity_descr = act_extractor.get_activities_dict_from_json(path_preprocessed_description)

    # 2. Transform to lists of activities for log and description based on dict of log and description
    list_activity_log = act_extractor.create_sentences_from_activity_dict(dict_activity_log)
    list_activity_descr = act_extractor.create_sentences_from_activity_dict(dict_activity_descr)

    # 3. First similarity check
    # Methods from similarity_measure folder
    if similarity_measure == "BERT":
        similarity_matrix, \
            most_similar_sentences, \
            corresponding_sentence_description, \
            corresponding_id_description, \
            corresponding_sentence_log, \
            corresponding_id_log, \
            corresponding_similarity_scores = \
            activity_similarity_check_one_bert(sentences_descr=list_activity_descr, sentences_log=list_activity_log)
    elif similarity_measure == "SPACY":
        similarity_matrix, \
            most_similar_sentences, \
            corresponding_sentence_description, \
            corresponding_id_description, \
            corresponding_sentence_log, \
            corresponding_id_log, \
            corresponding_similarity_scores = \
            activity_similarity_check_one_spacy(sentences_descr=list_activity_descr, sentences_log=list_activity_log)
    elif similarity_measure == "TF-IDF":
        similarity_matrix, \
            most_similar_sentences, \
            corresponding_sentence_description, \
            corresponding_id_description, \
            corresponding_sentence_log, \
            corresponding_id_log, \
            corresponding_similarity_scores = \
            activity_similarity_check_one_tfidf(sentences_descr=list_activity_descr, sentences_log=list_activity_log)
    else:
        raise ValueError("Wrong similarity measure was chosen. Either choose: BERT, tfi-df, or spacy!")

    # 4. Check intermediate results before continuing
    # If similarity is lower than threshold, replace the matched activity by an empty string
    list_log_activities_refined = \
        intermediate_one.remove_low_similarities_activity_check_one(similarities=corresponding_similarity_scores,
                                                                    list_of_string=most_similar_sentences,
                                                                    threshold=threshold)
    # Measurement types used to create the compliant outputs
    measurement_types = {"similarity_measure": similarity_measure,
                         "threshold": threshold,
                         "activity_matching": True
                         }

    # Return of results:
    # corresponding_id_description: List of ids of description which are matched in right order
    # corresponding_sentence_log: List of activities in log in matched order
    # corresponding_id_log: List of ids in log of activities in matched order
    # corresponding_similarity_score: similarities of matched activities in right order
    # list_log_activities_refined: matched activities with similarity higher than threshold or an empty string
    # measurement_types: measurement details, similarity approach, threshold info for activity check
    return corresponding_sentence_description, \
        corresponding_id_description, \
        corresponding_sentence_log, \
        corresponding_id_log, \
        corresponding_similarity_scores, \
        list_log_activities_refined, \
        measurement_types


def resource_activity_compliance_check_step_two(path_preprocessed_event_log: str,
                                                path_preprocessed_description: str,
                                                similarity_measure: str,
                                                threshold: float,
                                                resource_types: list,
                                                check_resource_and_activity: bool,
                                                perform_pattern_rar_check: bool
                                                ) -> Any:
    resource_types = literal_eval(resource_types)

    # 1. Activity check results
    corresponding_activities_description, \
        corresponding_id_description, \
        corresponding_activities_log, \
        corresponding_id_log, \
        corresponding_similarity_scores, \
        list_log_activities_refined, \
        measurement_types = \
        resource_activity_compliance_check_step_one(
            path_preprocessed_event_log=path_preprocessed_event_log,
            path_preprocessed_description=path_preprocessed_description,
            similarity_measure=similarity_measure,
            threshold=threshold
        )

    # 2. Get the Patterns for Activities and if needed the referenced id of the bonded activity
    corresponding_pattern_description = \
        check_and_return_pattern(pre_processed_description_path=path_preprocessed_description,
                                 matched_description_ids=corresponding_id_description
                                 )

    # 3. Create dictionaries of resource, (activity) pairs
    # Log
    if len(resource_types) == 1 and resource_types[0] == "user":
        list_log = res_act_extractor_log.create_user_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    elif len(resource_types) == 1 and resource_types[0] == "role":
        list_log = res_act_extractor_log.create_role_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    elif len(resource_types) == 1 and resource_types[0] == "org_unit":
        list_log = res_act_extractor_log.create_org_unit_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    elif len(resource_types) == 1 and resource_types[0] == "org":
        list_log = res_act_extractor_log.create_org_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    elif len(resource_types) == 2 and resource_types[0] == "user" and resource_types[1] == "role":
        list_log = res_act_extractor_log.create_user_and_role_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    elif len(resource_types) == 4 and resource_types[0] == "user" and resource_types[1] == "role" and \
            resource_types[2] == "org_unit" and resource_types[3] == "org":
        list_log = res_act_extractor_log.create_user_role_org_unit_and_org_activity_tuples_list(
            path_pre_processed_log=path_preprocessed_event_log,
            refined_activity_list_log=list_log_activities_refined,
            id_refined_log=corresponding_id_log,
            check_res_and_act=check_resource_and_activity
        )

    else:
        raise ValueError("Wrong input for resources are given!"
                         "Use either:"
                         "['user']"
                         "['role']"
                         "['org_unit']"
                         "['org']"
                         "['user']['role']"
                         "['user']['role']['org_unit']['org']")

    # Description
    list_descr = res_act_extractor_descr.create_resource_descr_activity_tuples_dict(
        path_preprocessed_description=path_preprocessed_description,
        activities_description_matched=corresponding_activities_description,
        id_matched_description=corresponding_id_description,
        check_res_and_act=check_resource_and_activity
    )

    # 4. Get again list of resource(-activity) strings, sentences if resource and activity was stored
    # It must be guaranteed, that the list_log has the same length as the list_descr.
    sentences_log = []
    sentences_descr = []

    # Resource Activity pairs
    if check_resource_and_activity:
        for i in range(0, len(list_log)):
            sentences_log.append(list_log[i][0] + " " + list_log[i][1])
            sentences_descr.append(list_descr[i][0] + " " + list_descr[i][1])
    # Only Resources to be checked
    else:
        sentences_log = list_log
        sentences_descr = list_descr

    # All data is given here: Now the Similarity check and verification process starts:
    # 5. Similarity check of resource-activity_check_one pairs of description and log
    if similarity_measure == "BERT":
        resources_checked_log, resources_checked_descr, res_check_similarity_scores = resource_activity_similarity_check_two_bert(
            resources_descr=sentences_descr, resources_matched_log=sentences_log
        )
    elif similarity_measure == "SPACY":
        resources_checked_log, resources_checked_descr, res_check_similarity_scores = resource_activity_similarity_check_two_spacy(
            resources_descr=sentences_descr, resources_matched_log=sentences_log
        )
    elif similarity_measure == "TF-IDF":
        resources_checked_log, resources_checked_descr, res_check_similarity_scores = resource_activity_similarity_check_two_tfidf(
            resources_descr=sentences_descr, resources_matched_log=sentences_log
        )
    else:
        raise ValueError("Wrong similarity measure was given. Please choose either: BERT, spacy, or tfi-df!")

    # Perform Pattern-based compliance check:
    if perform_pattern_rar_check:
        compliance_output = intermediate_two_pattern.pattern_based_rar_refinement(
            path_preprocessed_log=path_preprocessed_event_log,
            ids_of_log=corresponding_id_log,
            ids_of_description=corresponding_id_description,
            pattern_list=corresponding_pattern_description,
            activity_checks=list_log_activities_refined,
            resources_checked_log=resources_checked_log,
            resources_checked_description=resources_checked_descr,
            resources_similarity_scores=res_check_similarity_scores,
            threshold_resource_check=threshold
            )
        # Measurement types used to create the compliant outputs
        measurement_types = {"similarity_measure": similarity_measure,
                             "threshold": threshold,
                             "chosen_resource_combination_to_be_checked": resource_types,
                             "resource_activity_check_after_activity_check": check_resource_and_activity,
                             "resource_check_after_activity_check": not check_resource_and_activity,
                             "pattern_resource_compliant_check": True
                             }

    # Perform default resource-compliance check:
    else:

        compliance_output = intermediate_two_default.default_based_rar_refinement(
            path_preprocessed_log=path_preprocessed_event_log,
            ids_of_log=corresponding_id_log,
            ids_of_description=corresponding_id_description,
            pattern_list=corresponding_pattern_description,
            activity_checks=list_log_activities_refined,
            resources_checked_log=resources_checked_log,
            resources_checked_description=resources_checked_descr,
            resources_similarity_scores=res_check_similarity_scores,
            threshold_resource_check=threshold
        )

        # Measurement types used to create the compliant outputs
        measurement_types = {"Similarity_Measure": similarity_measure,
                             "Threshold": threshold,
                             "Chosen_Resource_Combination_to_be_Checked": resource_types,
                             "Resource_Activity_Check_after_Activity_Check": check_resource_and_activity,
                             "Resource_Check_after_Activity_Check": not check_resource_and_activity,
                             "Default_Resource_Compliance_Check": True
                             }

    # Return of results:
    return compliance_output, measurement_types
