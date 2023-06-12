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

import glob
import json
import os


def detect_and_add_patterns(pre_processed_description_path: str):
    # Get Json
    with open(pre_processed_description_path) as json_file:
        pre_processed_description_pair = json.load(json_file)
    # Get pre-processed description data
    pairs = pre_processed_description_pair["pairs"]

    patterns = []
    for pair in pairs:
        if pair["is_performed"]:
            if len(pair["exclusion"]) > 0:
                if pair["role"] != "not_specified":
                    patterns.append({"name": ["Static SoD", "Multi Bonded"], "id": [4, 6]})
                else:
                    patterns.append({"name": "Dynamic SoD", "id": 3})
            elif pair["equals"] or pair["min"] or pair["max"]:
                patterns.append({"name": "Multi-Segregated", "id": 5})
            elif len(pair["inclusion"]) == 1:
                patterns.append({"name": "Static Bonded", "id": 7})
            elif len(pair["inclusion"]) > 1:
                patterns.append({"name": "Multi Bonded", "id": 8})
            elif pair["resource"] == "automatic":
                patterns.append({"name": "Automatic", "id": 9})
            else:
                patterns.append({"name": "Performed by", "id": 1})
        else:
            patterns.append({"name": "Not Performed by", "id": 2})

    index = 0
    for pair in pairs:
        pair["pattern"] = patterns[index]
        index = index + 1

    new_json = {"pairs": pairs}

    __pre_processed_description_with_patterns(
        pre_processed_description_path=pre_processed_description_path,
        modified_data=new_json
    )
    return patterns


def __pre_processed_description_with_patterns(pre_processed_description_path: str, modified_data: dict):
    with open(pre_processed_description_path[:-5] + '_with_patterns.json', 'w') as file:
        json.dump(modified_data, file, indent=4)
