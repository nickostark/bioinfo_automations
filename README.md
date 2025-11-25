A collection of lightweight scripts I use to automate repetitive tasks in bioinformatics workflows.

## Scripts
`fastqc_summary.py`
Extracts all PASS/WARN/FAIL statuses from fastqc HTML reports for an entire project and consolidates them into a single CSV file.

### Usage
Modify `FASTQC_ROOT` & `OUTPUT_CSV` before execution.

Then run:
`python3 fastqc_summary.py <PROJECT_NAME>`

### How the result looks
<img width="717" height="544" alt="Screenshot0" src="https://github.com/user-attachments/assets/1dfb915a-fe95-486b-943c-d2046dd4ea44" />
