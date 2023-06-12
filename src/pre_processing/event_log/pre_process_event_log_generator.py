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
This file and the corresponding methods are responsible tp create the pre-processed event log which can be used for
resource-activity compliance verification.
"""
from pandas import DataFrame
import json

from dotenv import load_dotenv
import os

from extractors_pre_processing_event_log.extraction_to_data_frame import get_data_frame
from extractors_pre_processing_event_log.extraction_to_event_log import convert_df_to_event_log

load_dotenv()
HOME_PATH = os.environ['HOME_PATH']


def __load_data_frame(path: str, case_id_column_name: str, activity_column_name: str,
                      timestamp_key_name: str, used_separator: str) -> DataFrame:
    # Error checking
    possible_activity_id_column_names = ["", " "]
    if case_id_column_name in possible_activity_id_column_names and not activity_column_name == type(str):
        raise ValueError("Invalid activity_check_one name.")

    possible_case_id_column_names = ["", " "]
    if case_id_column_name in possible_case_id_column_names and not case_id_column_name == type(str):
        raise ValueError("Invalid case id/ trace id name.")

    possible_separators = [";", ",", ":", "-"]
    if used_separator not in possible_separators:
        raise ValueError("Invalid separator between column values. Expected one of: %s" % possible_separators)

    print("Data Frame loaded!")
    return get_data_frame(path, case_id_column_name, activity_column_name, timestamp_key_name, used_separator)


def create_event_log_pre_process_json(dataframe_input_path: str, case_id_column_name: str, activity_column_name: str,
                                      timestamp_key_name: str, used_separator: str, file_name: str, output_path: str):
    # csv dataframe
    dataframe = __load_data_frame(dataframe_input_path,
                                  case_id_column_name,
                                  activity_column_name,
                                  timestamp_key_name,
                                  used_separator)
    # Event Log based on dataframe, according to XES Meta model
    event_log = convert_df_to_event_log(df=dataframe)
    # List of: Case_Id, Event_Id, Resource, Activity, User, Organizational_Unit, Organization:
    resulting_list_of_dict = event_log.get_distinct_resource_activity_organisation_pairs_of_event_log()

    # Output data
    data = {"pairs": resulting_list_of_dict}
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    with open((output_path + file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    return json_output


# TEST
def __build_input_path(is_compliant: bool, event_log_path: str, event_log_name: str) -> str:
    if is_compliant not in [True, False]:
        raise ValueError("Please enter a boolean value for is_compliant")
    compliant_folder = "compliant" if is_compliant else "non_compliant"
    return event_log_path + f"/{compliant_folder}/{event_log_name}_log.csv"


def __build_output_path(log_path: str, output_folder_path: str):
    os.mkdir(output_folder_path)
    output_file = log_path.replace('input/logs', output_folder_path).replace('csv', 'json')
    # return output_file

    path = "pythonprog"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")

    # Create Directory and store files in it
    filename = "/foo/bar/baz.txt"
    os.makedirs(output_folder_path, True)
    with open(filename, "w") as f:
        f.write("FOOBAR")
