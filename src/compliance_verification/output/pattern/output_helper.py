"""
Create for pattern-based compliance check output JSON files
"""
import json
import os


def create_json_pattern_compliance_check(compliant_output: list[dict],
                                         measure_types: dict,
                                         file_name: str,
                                         output_path: str):
    output_dict = {"measure_types": measure_types,
                   "default_compliance_check_output": compliant_output
                   }
    # Generate json
    __generate_json_from_dict(output_dict=output_dict, file_name=file_name + "_pattern_compliant_output.json",
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
