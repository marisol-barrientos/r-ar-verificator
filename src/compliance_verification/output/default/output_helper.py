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
import json
import os





def create_json_default_compliance_check(compliant_output: list[dict],
                                         measure_types: dict,
                                         file_name: str,
                                         output_path: str):
    output_dict = {"measure_types": measure_types,
                   "default_compliance_check_output": compliant_output
                   }
    # Generate json
    __generate_json_from_dict(output_dict=output_dict, file_name=file_name + "_default_compliant_output.json",
                              output_path=output_path)


def __generate_json_from_dict(output_dict: dict, file_name: str, output_path: str):
    """
    :param output_dict.
    :type dict

    :param file_name.
    :type str

    :param output_path.
    :type str

    """
    # Output data
    json_output = json.dumps(output_dict, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path + file_name, 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=4, default=str)
    return json_output
