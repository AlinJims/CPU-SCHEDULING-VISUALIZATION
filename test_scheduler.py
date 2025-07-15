from src.process import Process
from src.scheduler import run_scheduling


# Sample processes
processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 1),
]

# Test FCFS
print("=== FCFS ===")
gantt_fcfs = run_scheduling("FCFS", processes.copy())
for entry in gantt_fcfs:
    print(f"Process {entry[0]}: Start {entry[1]}, End {entry[2]}")

# Recreate processes to reset their state
processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 1),
]

# Test SJF
print("\n=== SJF ===")
gantt_sjf = run_scheduling("SJF", processes)
for entry in gantt_sjf:
    print(f"Process {entry[0]}: Start {entry[1]}, End {entry[2]}")
