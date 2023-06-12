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

# Imports
from ..compliance_verification_process import resource_activity_compliance_check_step_one, \
    resource_activity_compliance_check_step_two

from .activity_matching.output_helper import create_compliant_json_activity_helper
from .default.output_helper import create_json_default_compliance_check
from .pattern.output_helper import create_json_pattern_compliance_check


def create_compliant_json_activity(path_preprocessed_event_log: str,
                                   path_preprocessed_description: str,
                                   similarity_measure: str,
                                   threshold: float,
                                   output_file_name: str,
                                   output_path: str
                                   ):

    # Get output of second activity check
    corresponding_sentence_description, corresponding_id_description, corresponding_sentence_log, corresponding_id_log, corresponding_similarity_scores, list_log_activities_refined, measurement_types = \
        resource_activity_compliance_check_step_one(
            path_preprocessed_event_log=path_preprocessed_event_log,
            path_preprocessed_description=path_preprocessed_description,
            similarity_measure=similarity_measure,
            threshold=threshold
        )
    # Create output of activity check
    create_compliant_json_activity_helper(path_pre_processed_event_log=path_preprocessed_event_log,
                                          path_pre_processed_description=path_preprocessed_description,
                                          activity_list=list_log_activities_refined,
                                          similarity_score_list=corresponding_similarity_scores,
                                          measure_types=measurement_types,
                                          output_file_name=output_file_name,
                                          output_path=output_path
                                          )

    # Add id to output file


def create_compliance_check_output(path_preprocessed_event_log: str,
                                   path_preprocessed_description: str,
                                   similarity_measure: str,
                                   threshold: float,
                                   resource_types_to_be_checked: list[str],
                                   check_resource_and_activity: bool,
                                   perform_pattern_rar_check: bool,
                                   file_name: str,
                                   output_path: str
                                   ):

    # Get output of second resource activity check
    # Resource-Activity List Log
    compliant_output, measurement_types = \
        resource_activity_compliance_check_step_two(path_preprocessed_event_log=path_preprocessed_event_log,
                                                    path_preprocessed_description=path_preprocessed_description,
                                                    similarity_measure=similarity_measure,
                                                    threshold=threshold,
                                                    resource_types=resource_types_to_be_checked,
                                                    check_resource_and_activity=check_resource_and_activity,
                                                    perform_pattern_rar_check=perform_pattern_rar_check
                                                    )

    if perform_pattern_rar_check:
        create_json_pattern_compliance_check(compliant_output=compliant_output,
                                             measure_types=measurement_types,
                                             file_name=file_name,
                                             output_path=output_path)

    else:
        create_json_default_compliance_check(compliant_output=compliant_output,
                                             measure_types=measurement_types,
                                             file_name=file_name,
                                             output_path=output_path)

    # Add id to output file
