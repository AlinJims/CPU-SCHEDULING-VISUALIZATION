from fcfs import fcfs_scheduling
from sjf import sjf_scheduling
from srtf import srtf_scheduling
from rr import rr_scheduling
from mlfq import mlfq_scheduling

def run_scheduling(algo, processes, quantum=None, time_quantums=None, context_delay=0): 
    print(f"[DEBUG] Running scheduling algorithm: {algo}")
    if algo == "FCFS":
        gantt = fcfs_scheduling(processes, context_delay=context_delay)
        return gantt, generate_metrics(processes)
    elif algo == "SJF":
        gantt = sjf_scheduling(processes, context_delay=context_delay)
        return gantt, generate_metrics(processes)
    elif algo == "SRTF":
        return srtf_scheduling(processes, context_delay=context_delay)
    elif algo == "RR":
        if quantum is None:
            raise ValueError("Quantum time required for Round Robin")
        return rr_scheduling(processes, quantum, context_delay=context_delay)
    elif algo == "MLFQ":
        return mlfq_scheduling(processes, time_quantums=time_quantums, context_delay=context_delay)
    else:
        raise ValueError(f"Unknown algorithm: {algo}")

def generate_metrics(processes):
    details = []
    total_tat = 0
    total_rt = 0
    for p in processes:
        tat = p.completion_time - p.arrival_time
        rt = p.response_time
        total_tat += tat
        total_rt += rt
        details.append({
            "pid": p.pid,
            "at": p.arrival_time,
            "bt": p.burst_time,
            "ct": p.completion_time,
            "tat": tat,
            "rt": rt
        })
    avg_tat = total_tat / len(processes)
    avg_rt = total_rt / len(processes)
    return {
        "details": details,
        "avg_tat": avg_tat,
        "avg_rt": avg_rt
    }
