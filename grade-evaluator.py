"""
Grade Evaluator & Archiver
---------------------------
Author: emutoniwas-code

Calculates a student's final academic standing from a CSV file of
course grades. Built on top of the provided starter template
(load_csv_data / evaluate_grades).

Expected CSV columns: assignment, group, score, weight
    assignment -> name of the assignment
    group      -> "Summative" or "Formative"
    score      -> score obtained (0-100)
    weight     -> weight of the assignment (out of 100 overall)
"""

import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print(f"Error: '{filename}' is empty. There is no data to evaluate.")
                sys.exit(1)

            for i, row in enumerate(reader, start=2):  # start=2: header is line 1
                # Skip fully blank rows
                if not any((row.get(k) or "").strip() for k in row):
                    continue

                group = (row.get('group') or "").strip().title()
                if group not in ("Summative", "Formative"):
                    print(f"Error: Row {i} has an invalid group '{group}'. "
                          f"Expected 'Summative' or 'Formative'.")
                    sys.exit(1)

                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except (ValueError, KeyError) as e:
                    print(f"Error: Row {i} has a missing or non-numeric "
                          f"score/weight ({e}).")
                    sys.exit(1)

                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': group,
                    'score': score,
                    'weight': weight
                })

        if not assignments:
            print(f"Error: '{filename}' has no assignment rows to evaluate.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    'data' is a list of dictionaries containing the assignment records.

    a) Checks all scores are percentage based (0-100)
    b) Validates total weights (Total=100, Summative=40, Formative=60)
    c) Calculates the Final Grade and GPA
    d) Determines Pass/Fail status (>= 50% in BOTH categories)
    e) Checks for failed formative assignments (< 50) and determines
       which one(s) have the highest weight, for resubmission
    f) Prints the final decision (PASSED / FAILED) and resubmission options
    """
    print("\n--- Processing Grades ---")

    # a) Grade validation: every score must be within 0-100
    for row in data:
        if not (0 <= row['score'] <= 100):
            print(f"Error: '{row['assignment']}' has an invalid score "
                  f"({row['score']}). Scores must be between 0 and 100.")
            sys.exit(1)

    # b) Weight validation: Total=100, Summative=40, Formative=60
    total_weight = sum(r['weight'] for r in data)
    summative_weight = sum(r['weight'] for r in data if r['group'] == 'Summative')
    formative_weight = sum(r['weight'] for r in data if r['group'] == 'Formative')

    errors = []
    if round(total_weight, 4) != 100:
        errors.append(f"Total weight is {total_weight}, expected exactly 100.")
    if round(summative_weight, 4) != 40:
        errors.append(f"Summative weight is {summative_weight}, expected exactly 40.")
    if round(formative_weight, 4) != 60:
        errors.append(f"Formative weight is {formative_weight}, expected exactly 60.")

    if errors:
        print("Error: Weight validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # c) Calculate the Final Grade and GPA
    def category_percentage(group_name, cat_weight_total):
        cat_rows = [r for r in data if r['group'] == group_name]
        weighted_points = sum((r['weight'] * r['score']) / 100 for r in cat_rows)
        # weighted_points is out of cat_weight_total (40 or 60)
        return (weighted_points / cat_weight_total) * 100 if cat_weight_total else 0.0

    summative_pct = category_percentage('Summative', summative_weight)
    formative_pct = category_percentage('Formative', formative_weight)
    final_grade = sum((r['weight'] * r['score']) / 100 for r in data)  # out of 100
    gpa = (final_grade / 100) * 5.0

    # d) Pass/Fail: >= 50% in BOTH categories
    passed = summative_pct >= 50 and formative_pct >= 50
    status = "PASSED" if passed else "FAILED"

    # Report
    for r in data:
        print(f"  [{r['group']:<10}] {r['assignment']:<40} "
              f"weight={r['weight']:<5} score={r['score']}")
    print("-" * 60)
    print(f"Summative category score: {summative_pct:.2f}%  (weight allotment: 40)")
    print(f"Formative category score: {formative_pct:.2f}%  (weight allotment: 60)")
    print(f"Final Grade:               {final_grade:.2f}/100")
    print(f"Final GPA:                 {gpa:.2f}/5.0")
    print(f"Final Status:              {status}")

    # e) Resubmission: failed (score < 50) Formative assignment(s) with
    #    the highest weight. Ties -> all listed.
    if not passed:
        failed_formatives = [
            r for r in data if r['group'] == 'Formative' and r['score'] < 50
        ]
        if failed_formatives:
            max_weight = max(r['weight'] for r in failed_formatives)
            candidates = [r for r in failed_formatives if r['weight'] == max_weight]
            names = ", ".join(c['assignment'] for c in candidates)
            print(f"Eligible for resubmission (highest-weight failed "
                  f"Formative assignment(s)): {names}")
        else:
            print("No failed Formative assignments found, so no "
                  "resubmission is applicable.")
    print("=" * 60)


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    # 2. Process the features
    evaluate_grades(course_data)
