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
- This file provides a function (get_data_frame), which requires a path to a csv file as parameter
and returns a dataframe in right format for further process log analysis
"""
# Required Imports:
import pandas as pd
import pm4py as pm


# Based on the Path and the most important Log Attributes, create a Pandas DataFrame
def get_data_frame(path: str, case_id_name: str, activity_key_name: str, timestamp_key_name: str, sep: str):
    # First import the csv file and convert the csv file to an Event Log
    df = pd.read_csv(filepath_or_buffer=path, sep=sep)
    df = pm.format_dataframe(df=df,
                             case_id=case_id_name,
                             activity_key=activity_key_name,
                             timestamp_key=timestamp_key_name)
    # Drop old case id column, axis =1 means column
    df = df.drop(columns=[case_id_name])
    return df
