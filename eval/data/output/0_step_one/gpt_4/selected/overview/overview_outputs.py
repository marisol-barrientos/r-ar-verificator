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
import json

bicycle_file_path = "../1-bicycle_manufacturing-gpt-4.json"
schedule_metting_file_path = "../1-schedule_meetings_creation_next_year.json"
bpic_file_path = "../1-BPI_2020_C_PF_D-gpt-4.json"
running_example_file_path = "../2-running_example_v3-gpt-4.json"

with open(running_example_file_path, "r") as f1:
    data = json.load(f1)

pairs = data["pairs"]

# Initialize counters
total_pairs = len(pairs)
anaphora_true = 0
condition_true = 0
performed_true = 0
non_empty_inclusion = 0
non_empty_exclusion = 0
non_empty_min = 0
non_empty_max = 0
non_empty_equals = 0
role_not_specified = 0
user_not_specified = 0
org_unit_not_specified = 0
organization_not_specified = 0

# Iterate through pairs and update counters
for pair in pairs:
    if pair["has_anaphora"][0]:
        anaphora_true += 1
    if pair["has_condition"][0]:
        condition_true += 1
    if pair["is_performed"]:
        performed_true += 1
    if pair["inclusion"]:
        non_empty_inclusion += 1
    if pair["exclusion"]:
        non_empty_exclusion += 1
    if pair["min"]:
        non_empty_min += 1
    if pair["max"]:
        non_empty_max += 1
    if pair["equals"]:
        non_empty_equals += 1
    if pair["role"] in ["not_specified", ""]:
        role_not_specified += 1
    if pair["user"] in ["not_specified", ""]:
        user_not_specified += 1
    if pair["org_unit"] in ["not_specified", ""]:
        org_unit_not_specified += 1
    if pair["organization"] in ["not_specified", ""]:
        organization_not_specified += 1

# Print results
print("Total number of pairs:", total_pairs)
print("Number of pairs with has_anaphora = true:", anaphora_true)
print("Number of pairs with has_condition = true:", condition_true)
print("Number of pairs with is_performed = true:", performed_true)
print("Total number of inclusion not empty:", non_empty_inclusion)
print("Total number of exclusion not empty:", non_empty_exclusion)
print("Total number of min not empty:", non_empty_min)
print("Total number of max not empty:", non_empty_max)
print("Total number of equals not empty:", non_empty_equals)
print("Total number of role not_specified or empty:", role_not_specified)
print("Total number of user not_specified or empty:", user_not_specified)
print("Total number of org_unit not_specified or empty:", org_unit_not_specified)
print("Total number of organization not_specified or empty:", organization_not_specified)

# Save results to a text file
with open("running_example_overview.txt", "w") as output_file:
    output_file.write("Total number of pairs: " + str(total_pairs) + "\n")
    output_file.write("Number of pairs with has_anaphora = true: " + str(anaphora_true) + "\n")
    output_file.write("Number of pairs with has_condition = true: " + str(condition_true) + "\n")
    output_file.write("Number of pairs with is_performed = true: " + str(performed_true) + "\n")
    output_file.write("Total number of inclusion not empty: " + str(non_empty_inclusion) + "\n")
    output_file.write("Total number of exclusion not empty: " + str(non_empty_exclusion) + "\n")
    output_file.write("Total number of min not empty: " + str(non_empty_min) + "\n")
    output_file.write("Total number of max not empty: " + str(non_empty_max) + "\n")
    output_file.write("Total number of equals not empty: " + str(non_empty_equals) + "\n")
    output_file.write("Total number of role not_specified or empty: " + str(role_not_specified) + "\n")
    output_file.write("Total number of user not_specified or empty: " + str(user_not_specified) + "\n")
    output_file.write("Total number of org_unit not_specified or empty: " + str(org_unit_not_specified) + "\n")
    output_file.write("Total number of organization not_specified or empty: " + str(organization_not_specified) + "\n")

print("Results saved to output.txt")