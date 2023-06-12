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

bicycle_manufacturing_eval_last_step = "bicycle_manufacturing_eval_last_step.json"
non_bicycle_manufacturing_eval_last_step = "non_bicycle_manufacturing_eval_last_step.json"
non_running_example_v3_eval_last_step = "non_running_example_v3_eval_last_step.json"
non_schedule_meetings_creation_next_year_eval_last_step = "non_schedule_meetings_creation_next_year_eval_last_step.json"
running_example_v3_eval_last_step = "running_example_v3_eval_last_step.json"
schedule_meetings_creation_next_year_eval_last_step = "schedule_meetings_creation_next_year_eval_last_step.json"

all = [bicycle_manufacturing_eval_last_step, non_bicycle_manufacturing_eval_last_step, non_running_example_v3_eval_last_step,
       non_schedule_meetings_creation_next_year_eval_last_step, running_example_v3_eval_last_step, schedule_meetings_creation_next_year_eval_last_step]

def calculate_scores(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    tp = len(data['true_positive'])
    tn = len(data['true_negative'])
    fp = len(data['false_positive'])
    fn = len(data['false_negative'])

    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return {
        'True Positive': tp,
        'True Negative': tn,
        'False Positive': fp,
        'False Negative': fn,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }

# Usage
for json_file_path in all:
    print(calculate_scores(json_file_path))