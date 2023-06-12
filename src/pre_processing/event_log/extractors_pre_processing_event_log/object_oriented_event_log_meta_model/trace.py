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
This file consists of the class Trace which gets as parameter a unique case id and a List of Events
The class Trace implements some functions which help to understand the respective process execution
"""

# Required Imports:
from typing import List

# Imported class
from .event import Event


# Trace class depends on the existence of an Event Log
class Trace:

    def __init__(self, case_id: str, events: List[Event]) -> None:
        self.case_id = case_id
        self.events = events

    # Returns a dict object with case_id as key and all resource, activity_check_one pairs (:= event) as value
    def get_resource_activity_organisation_structure_pairs_of_trace(self) -> dict:
        case_id = self.case_id
        trace_pair = {}
        res_act_pairs = []
        for e in self.events:
            res_act_pair = e.get_resource_activity_organisation_structure_pair()
            res_act_pairs.append(res_act_pair)
        trace_pair[case_id] = res_act_pairs
        return trace_pair
