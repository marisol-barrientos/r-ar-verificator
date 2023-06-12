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
This file consists of the class EventLog which requires as Parameter a List of Traces

The class implements several functions which provide insights of the current process log
and therefore for the real process executions
"""

import os
# Required Imports:
from typing import List, Union, Any

from dotenv import load_dotenv


# Imported class
from .trace import Trace


# Object-oriented structure of the XES Document UML Model for Event Logs
class EventLog:

    def __init__(self, traces: List[Trace]) -> None:
        self.traces = traces

    # Return List of: Case_Id, Event_Id, Resource, Activity, User, Organizational_Unit, Organization:
    def get_distinct_resource_activity_organisation_pairs_of_event_log(self) -> list[
        dict[str, Union[int, dict[Any, list[str]]]]]:

        resulting_list_of_dict = []
        res_act_org_dict = self.__get__resource_activity_organisation_pairs_of_event_log()

        # Go through all case_ids -> consist of a list of dicts
        counting_id = 1

        for case_id, list_of_events in res_act_org_dict.items():

            # Go through the values of the event log for one trace
            for res_act_org_values in list_of_events:
                event_id = res_act_org_values.get("event_id", "u")
                #print(event_id)
                activity = res_act_org_values.get("Activity", "u")
                time = res_act_org_values.get("Timestamp", "u")
                lifecycle = res_act_org_values.get("Lifecycle_Transition", "u")
                resource = res_act_org_values.get("Resource", "u")
                role = res_act_org_values.get("Role", "u")
                org_unit = res_act_org_values.get("Organizational_Unit", "u")
                org = res_act_org_values.get("Organization", "u")

                # Value from log to compare
                compare_from_value = activity + " " + resource + " " + role + " " + org_unit + " " + org
                has_same = False

                # Check if Activity,User,Org unit,Organisation already exist:
                for resulting_dict in resulting_list_of_dict:
                    compare_with_value = resulting_dict["activity"] + " " + (
                            resulting_dict["user"] + " " + resulting_dict["role"] + " " + resulting_dict["org_unit"] +
                            " " + resulting_dict["organization"])

                    # Add case id to the case id list and add event id to the event id list
                    if compare_from_value == compare_with_value:

                        # Add the id's of the same dict
                        id_existing = resulting_dict["case_id"]

                        has_case_id = False
                        for cid in id_existing.keys():
                            if cid == case_id:
                                has_case_id = True
                        # Check if case id already exist
                        if has_case_id:
                            # add event id to list
                            id_existing[case_id].append(str(event_id) + ", " + lifecycle + ", " + str(time))
                        else:
                            # create new entry with case_id as key and list of event ids   
                            id_existing[case_id] = [str(event_id) + ", " + lifecycle + ", " + str(time)]

                        resulting_dict["case_id"] = id_existing

                        # Set to true if already has been filled with values
                        has_same = True

                if len(resulting_list_of_dict) == 0 or not has_same:
                    # ID of event: case id and event_id
                    id_case_event = {case_id: [str(event_id) + ", " + lifecycle + ", " + str(time)]}
                    # New dict: storing the event log information
                    resulting_dict = {"id": counting_id, "case_id": id_case_event, "activity": activity,
                                      "user": resource, "role": role, "org_unit": org_unit, "organization": org}

                    # resulting_dict["timestamp"] = time
                    # resulting_dict["lifecycle_transition"] = lifecycle

                    resulting_list_of_dict.append(resulting_dict)

                    # Increase the counting id
                    counting_id = counting_id + 1

        return resulting_list_of_dict

    # Returns all resource activity_check_one pairs of the event log
    # @private
    def __get__resource_activity_organisation_pairs_of_event_log(self) -> dict:
        res_act_pairs_of_traces = {}
        for t in self.traces:
            dict_res_act = t.get_resource_activity_organisation_structure_pairs_of_trace()
            for key, value in dict_res_act.items():
                res_act_pairs_of_traces[key] = value
        return res_act_pairs_of_traces
