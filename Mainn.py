import subprocess

# List of files to run
files_to_run = ["raid.py", "main.py"]

processes = []

for file in files_to_run:
    print(f"Running {file}...")
    # Start the script in a new process
    process = subprocess.Popen(['python', file])
    processes.append(process)

# Optionally wait for all processes to finish
for process in processes:
    process.wait()
