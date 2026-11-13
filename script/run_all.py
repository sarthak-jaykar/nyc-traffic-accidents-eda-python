"""Run the full pipeline in order: ingest, clean, features, analysis, charts."""
import subprocess
import sys
from pathlib import Path

STEPS = ["01_ingest.py", "02_clean.py", "03_features.py", "04_analysis.py", "05_charts.py"]

def main():
    here = Path(__file__).resolve().parent
    for step in STEPS:
        print(f"\n=== {step} ===")
        result = subprocess.run([sys.executable, str(here / step)], cwd=here)
        if result.returncode != 0:
            sys.exit(f"Step failed: {step}")
    print("\nPipeline complete. Results in results/ and screenshots/.")

if __name__ == "__main__":
    main()
