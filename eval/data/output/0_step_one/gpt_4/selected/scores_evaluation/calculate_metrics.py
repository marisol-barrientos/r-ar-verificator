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
def calculate_metrics(tp, tn, fp, fn):
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if tp + tn + fp + fn > 0 else 0
    return precision, recall, f1_score, accuracy

input_file = "evaluation_first_step_summary.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

results = []

for line in lines:
    line = line.strip()
    parts = line.split(" = ")

    model_name = parts[0].strip()
    values = parts[1].strip()
    tn, tp, fp, fn = [int(val.split(": ")[1]) for val in values.split(", ")]

    precision, recall, f1_score, accuracy = calculate_metrics(tp, tn, fp, fn)
    result = {
        "model": model_name,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "accuracy": accuracy
    }
    results.append(result)

# Print results
with open("calculate_metrics_first_step.txt", "w") as output_file:
    for result in results:
        print(f"{result['model']}:")
        print(f"  Precision: {result['precision']:.2f}")
        print(f"  Recall: {result['recall']:.2f}")
        print(f"  F1-score: {result['f1_score']:.2f}")
        print(f"  Accuracy: {result['accuracy']:.2f}")
        print()
        output_file.write(f"{result['model']}:"+ "\n")
        output_file.write(f"  Precision: {result['precision']:.2f}" + "\n")
        output_file.write(f"  Recall: {result['recall']:.2f}" + "\n")
        output_file.write(f"  F1-score: {result['f1_score']:.2f}" + "\n")
        output_file.write(f"  Accuracy: {result['accuracy']:.2f}"+ "\n")
        output_file.write("\n")


def compare_results(result1, result2):
    improvements = {}
    for metric in ["precision", "recall", "f1_score", "accuracy"]:
        improvement = ((result2[metric] - result1[metric]) / result1[metric]) * 100
        improvements[metric] = improvement
    return improvements


# ... (previous code)

# Compare consecutive pairs of records and print the improvements
with open("calculate_improvements_first_step.txt", "w") as output_file:
    for i in range(0, len(results), 2):
        result1 = results[i]
        result2 = results[i + 1]

        improvements = compare_results(result1, result2)

        output_file.write(f"Improvements for {result2['model']} compared to {result1['model']}:\n")
        for metric, improvement in improvements.items():
            output_file.write(f"  {metric.capitalize()}: {improvement:.2f}%\n")
        output_file.write("\n")
