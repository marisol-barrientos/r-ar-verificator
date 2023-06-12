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
- This file imports the structure based on the XES Process Log UML Meta-Model
XES UML Meta Model: Event Log <>- (contains) - Traces <>- (contains) <>- Events <>- (contains) - Attributes
"""
# Required Imports:
import pandas as pd

from .object_oriented_event_log_meta_model.event_log import EventLog
from .object_oriented_event_log_meta_model.trace import Trace
from .object_oriented_event_log_meta_model.event import Event
from .object_oriented_event_log_meta_model.attribute import Attribute


# Convert Dataframe to Event Log of own implemented class
def convert_df_to_event_log(df: pd.DataFrame):
    if type(df) is not type(pd.DataFrame):
        ValueError("Wrong input data!")

    case_ids = df['case:concept:name']
    cases = list(dict.fromkeys(case_ids))
    traces = []

    for case in cases:
        event = None
        # Get the events as data frame of the given trace
        case_df = df.loc[df["case:concept:name"] == case]
        # Get all event values
        events_values = case_df.values.tolist()
        # Get all event attribute keys
        attrib_keys = df.columns.tolist()
        events_of_trace = []
        for event_values in events_values:
            event_attributes = []
            i = 0
            # Create tuple with attrib and value
            for attrib_key in attrib_keys:
                # Case_id and unnecessary attrib
                if attrib_key != 'case:concept:name' and attrib_key != '@@index':
                    attrib = Attribute(attrib_key, event_values[i])
                    i = i + 1
                    # Stores one Event from a Trace
                    event_attributes.append(attrib)
                    event = Event(event_attributes)
            events_of_trace.append(event)
        # Store Trace of Event Log
        trace = Trace(case, events_of_trace)
        #print(trace)
        traces.append(trace)

    # Event Log
    return EventLog(traces)
