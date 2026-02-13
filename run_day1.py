import os
import subprocess
import time

print("DAY 1 PIPELINE - SEQUENTIAL EXECUTION\n")

def run_step(step_name, cmd):
    print(f"[{step_name}] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[ERROR {step_name}]:", result.stderr)
    time.sleep(1)  # Prevent overload
    return result.returncode == 0

# Sequential: H2 → H3-H4 → H5 → H6-H7
steps = [
    ("H2", "cd src && python generate_monaco_data.py"),
    ("H3-H4", "cd src && python clean_data.py"), 
    ("H5", "cd src && python create_schema.py"),
    ("H6-H7", "cd src && python etl_core.py")
]

success = True
for step_name, cmd in steps:
    if not run_step(step_name, cmd):
        success = False
        print(f"\n[FAILED] {step_name} - Check manually!")
        break

if success:
    print("\n" + "="*50)
    print("DAY1 SUCCESS! 72 Monaco pits in PostgreSQL!")
    print("Check: data/clean/monaco_clean.tsv | pgAdmin | images/")
    print("="*50)
else:
    print("\nPipeline stopped. Fix errors above then re-run failed steps.")
