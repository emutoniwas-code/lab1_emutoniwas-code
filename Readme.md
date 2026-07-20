# Lab 1: Grade Evaluator & Archiver

Calculates a student's final academic standing from `grades.csv`, and
archives/resets the CSV file using a Bash organizer script.

## Files in this repo

- `grade-evaluator.py` — reads a `grades.csv` file you supply, validates
  it, calculates the final GPA, prints PASSED/FAILED, and identifies
  which failed Formative assignment(s) are eligible for resubmission.
- `organizer.sh` — archives the current `grades.csv` into `archive/` with
  a timestamped filename, resets a fresh empty `grades.csv`, and logs
  every run to `organizer.log`.
- `Readme.md` — this file.

**Note:** `grades.csv` is not included in this repo. You need to create
your own in the same folder before running either script — see the
format below.

## `grades.csv` format

The evaluator expects a CSV with these columns:

| Column     | Description                          |
|------------|---------------------------------------|
| assignment | Name of the assignment                |
| group      | `Summative` or `Formative`            |
| score      | Score obtained (0–100)                |
| weight     | Weight of the assignment (out of 100) |

Example:

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

Formative weights must sum to exactly **60**, Summative weights must sum
to exactly **40**, for a total of exactly **100**.

## Running the grade evaluator

```bash
python3 grade-evaluator.py
```

The script prompts for a filename (type `grades.csv` and press Enter),
then prints a report including:

- Each assignment with its group, weight, and score
- Summative and Formative category percentages
- Final Grade and GPA (`GPA = (Final Grade / 100) * 5.0`)
- Final status: **PASSED** (requires ≥50% in *both* Summative and
  Formative) or **FAILED**
- If failed, which Formative assignment(s) with the highest weight are
  eligible for resubmission

The script exits with a clear error message if the file is missing,
empty, has an invalid group, non-numeric scores/weights, out-of-range
scores, or a weight sum that doesn't match the 60/40/100 split.

## Running the organizer script

```bash
chmod +x organizer.sh   # only needed once
./organizer.sh
```

Each run will:

1. Create an `archive/` directory if it doesn't already exist.
2. Rename the current `grades.csv` to `grades_<TIMESTAMP>.csv` and move
   it into `archive/`.
3. Create a fresh, empty `grades.csv`.
4. Append an entry to `organizer.log`. Entries accumulate across runs.

## Typical workflow

```bash
python3 grade-evaluator.py   # evaluate the current grades.csv
./organizer.sh                # archive it and reset the workspace
```

## Author

emutoniwas-code
