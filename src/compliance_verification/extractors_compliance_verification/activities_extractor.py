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

from typing import List
import json


# Filter Activities from json file (either description or log file)
def get_activities_dict_from_json(path: str) -> dict:
    # Store dict with {id: activity_check_one}
    activities_dict = {}
    # Get json file
    with open(path) as file:
        json_data = json.load(file)
    # List of distinct events
    pairs = json_data["pairs"]
    # Iterate through the list
    for distinct_event in pairs:
        # Id (counting)
        id = distinct_event["id"]
        # Activity
        activity = distinct_event["activity"]
        # Add id and activity_check_one to dict
        activities_dict[id] = activity
    # Return dict {id: activity_check_one}
    return activities_dict


# Create activities as string in a list from activity_check_one dictionary
def create_sentences_from_activity_dict(activity_dict: dict) -> List[str]:
    return list(activity_dict.values())


# Create activity_check_one dictionary from the list of similar activities
def create_activity_dict_from_similarity_list(activity_list: dict) -> dict:
    # Store dict with {id: activity_check_one}
    activity_dict = {}
    count = 1
    for activity in activity_list:
        activity_dict[count] = activity
        count = count + 1
    return activity_dict
