from collections import deque

def mlfq_scheduling(processes, time_quantums=[4, 8, 12, 16], allotments=[8, 16, 24, float('inf')], context_delay=0):
    num_levels = len(time_quantums)
    queues = [deque() for _ in range(num_levels)]
    time = 0
    idx = 0
    n = len(processes)
    gantt = []
    completed = 0
    response_time_set = set()
    last_pid = None  

    for p in processes:
        p.queue_level = 0
        p.remaining_allotment = allotments[0]

    processes.sort(key=lambda p: p.arrival_time)

    queues[0].append(processes[0])
    idx = 1

    while completed < n:
        for level in range(num_levels):
            if queues[level]:
                q = queues[level]
                p = q.popleft()

             
                if last_pid is not None and last_pid != p.pid and context_delay > 0:
                    gantt.append(("CS", time, time + context_delay))
                    time += context_delay

                if p.pid not in response_time_set:
                    p.response_time = time - p.arrival_time
                    response_time_set.add(p.pid)

                qtime = min(time_quantums[level], p.remaining_time)
                start = time
                end = time + qtime

                gantt.append((f"{p.pid}(Q{level})", start, end))

                time += qtime
                p.remaining_time -= qtime
                p.remaining_allotment -= qtime

            
                while idx < n and processes[idx].arrival_time <= time:
                    processes[idx].queue_level = 0
                    processes[idx].remaining_allotment = allotments[0]
                    queues[0].append(processes[idx])
                    idx += 1

                if p.remaining_time <= 0:
                    p.completion_time = time
                    completed += 1
                else:
                    if p.remaining_allotment <= 0 and p.queue_level + 1 < num_levels:
                        p.queue_level += 1
                        p.remaining_allotment = allotments[p.queue_level]
                    queues[p.queue_level].append(p)

                last_pid = p.pid  
                break
        else:
         
            if idx < n:
                queues[0].append(processes[idx])
                time = processes[idx].arrival_time
                idx += 1

    total_tat = 0
    total_rt = 0
    metrics = []

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
