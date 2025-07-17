import heapq

def srtf_scheduling(processes, context_delay=0):
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    ready_queue = []
    metrics = []
    idx = 0

    remaining_times = {p.pid: p.burst_time for p in processes}
    last_execution = {}
    response_times = {}
    completion_times = {}
    is_started = set()
    prev_pid = None

    while completed < n:
        while idx < n and processes[idx].arrival_time <= current_time:
            heapq.heappush(ready_queue, (remaining_times[processes[idx].pid], processes[idx].arrival_time, processes[idx]))
            idx += 1

        if ready_queue:
            rem_bt, _, current_process = heapq.heappop(ready_queue)
            pid = current_process.pid

      
            if prev_pid is not None and prev_pid != pid and context_delay > 0:
                gantt_chart.append(("CS", current_time, current_time + context_delay))
                current_time += context_delay

            if pid not in is_started:
                response_times[pid] = current_time - current_process.arrival_time
                is_started.add(pid)

            if gantt_chart and gantt_chart[-1][0] == pid:
                gantt_chart[-1] = (pid, gantt_chart[-1][1], current_time + 1)
            else:
                gantt_chart.append((pid, current_time, current_time + 1))

            remaining_times[pid] -= 1
            current_time += 1

            if remaining_times[pid] > 0:
                heapq.heappush(ready_queue, (remaining_times[pid], current_process.arrival_time, current_process))
            else:
                completed += 1
                completion_times[pid] = current_time

            prev_pid = pid  
        else:
            current_time += 1

    total_tat = 0
    total_rt = 0
    for p in processes:
        ct = completion_times[p.pid]
        tat = ct - p.arrival_time
        rt = response_times[p.pid]
        total_tat += tat
        total_rt += rt
        metrics.append({
            "pid": p.pid,
            "at": p.arrival_time,
            "bt": p.burst_time,
            "ct": ct,
            "tat": tat,
            "rt": rt
        })

    avg_tat = total_tat / n
    avg_rt = total_rt / n

    return gantt_chart, {"details": metrics, "avg_tat": avg_tat, "avg_rt": avg_rt}
