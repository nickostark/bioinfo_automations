"""
This script automatically extracts PASS/WARN/FAIL statuses from all fastQC HTML reports. 
It parses each report’s summary section and outputs a consolidated QC overview CSV for the entire project.
Version based on which this script was written: fastqc/0.11.9
Modify `FASTQC_ROOT` & `OUTPUT_CSV` before execution.
"""

# To run the script 'python3 fastqc_summary.py [PROJECT_NAME]'

import os
import csv
import sys
from bs4 import BeautifulSoup

def parse_fastqc_html(html_file):
    """Extract (module_name, status) from one fastQC html report."""
    results = []

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    summary_div = soup.find("div", {"class": "summary"})
    if not summary_div:
        return results

    items = summary_div.find_all("li")
    for item in items:
        img = item.find("img")
        a = item.find("a")

        if img and a:
            # Status is inside the alt text, e.g. "[PASS]"
            status = img.get("alt", "").strip("[] ")

            # Module name is the link text
            module = a.get_text(strip=True)

            results.append((module, status))

    return results


def main():
    # ---------------------------------------------
    # Parse PROJECT_NAME from command-line argument
    # ---------------------------------------------
    if len(sys.argv) != 2:
        print("Usage: python fastqc_summary.py <PROJECT_NAME>")
        sys.exit(1)
    
    PROJECT_NAME = sys.argv[1]

    FASTQC_ROOT = f"~/{PROJECT_NAME}/fastqc"
    OUTPUT_CSV = f"~/{PROJECT_NAME}_qc_summary.csv"

    summary = []

    for root, dirs, files in os.walk(FASTQC_ROOT):
        for file in files:
            if file.endswith("_fastqc.html"):
                html_path = os.path.join(root, file)

                base = file.replace("_fastqc.html", "")
                parts = base.split("_")
                sample_id = parts[0]
                read = parts[1] if len(parts) > 1 else "unknown"

                qc_results = parse_fastqc_html(html_path)

                for module, status in qc_results:
                    summary.append([sample_id, read, module, status])

    # Write CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample", "read", "module", "status"])
        writer.writerows(summary)

    print(f"Saved summary to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()



