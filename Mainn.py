import os

# List of files to run
files_to_run = ["raid.py", "main.py"]

for file in files_to_run:
    print(f"Running {file}...")
    os.system(f"python {file}")
