# rr.py
from collections import deque

def rr_scheduling(processes, quantum):
    queue = deque()
    processes.sort(key=lambda p: p.arrival_time)
    time = 0
    idx = 0
    completed = 0
    n = len(processes)
    gantt = []
    response_time_set = set()
    metrics = []

    queue.append(processes[0])
    idx = 1

    while completed < n:
        if not queue:
            if idx < n:
                queue.append(processes[idx])
                time = processes[idx].arrival_time
                idx += 1
            continue

        p = queue.popleft()
        start = time
        if p.pid not in response_time_set:
            p.response_time = start - p.arrival_time
            response_time_set.add(p.pid)

        run_time = min(quantum, p.remaining_time)
        time += run_time
        p.remaining_time -= run_time
        gantt.append((p.pid, start, time))

        while idx < n and processes[idx].arrival_time <= time:
            queue.append(processes[idx])
            idx += 1

        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = time
            completed += 1

    total_tat = 0
    total_rt = 0
    for p in processes:
        tat = p.completion_time - p.arrival_time
        total_tat += tat
        total_rt += p.response_time
        metrics.append({
            "pid": p.pid,
            "at": p.arrival_time,
            "bt": p.burst_time,
            "ct": p.completion_time,
            "tat": tat,
            "rt": p.response_time
        })

    avg_tat = total_tat / n
    avg_rt = total_rt / n

    return gantt, {"details": metrics, "avg_tat": avg_tat, "avg_rt": avg_rt}
