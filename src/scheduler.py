# src/scheduler.py

from fcfs import simulate_fcfs
from sjf import simulate_sjf

def run_scheduling(algorithm, processes):
    if algorithm == "FCFS":
        return simulate_fcfs(processes)
    elif algorithm == "SJF":
        return simulate_sjf(processes)
    else:
        raise ValueError(f"Unsupported scheduling algorithm: {algorithm}")
