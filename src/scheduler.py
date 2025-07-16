from fcfs import fcfs_scheduling
from sjf import sjf_scheduling
from srtf import srtf_scheduling


def run_scheduling(algo, processes):
    if algo == "FCFS":
        return fcfs_scheduling(processes)
    elif algo == "SJF":
        return sjf_scheduling(processes)
    elif algo == "SRTF":
        return srtf_scheduling(processes)
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")
