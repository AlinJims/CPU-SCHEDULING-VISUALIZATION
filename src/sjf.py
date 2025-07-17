def sjf_scheduling(processes, context_delay=0):
    processes.sort(key=lambda p: (p.arrival_time, p.burst_time))
    time = 0
    completed = 0
    n = len(processes)
    gantt_chart = []
    is_completed = [False] * n
    last_pid = None  # To track last executed process

    while completed != n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            p = processes[i]
            if p.arrival_time <= time and not is_completed[i]:
                if p.burst_time < min_bt:
                    min_bt = p.burst_time
                    idx = i
                elif p.burst_time == min_bt:
                    if p.arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            p = processes[idx]

            # Apply context switch delay if needed (and not first process)
            if last_pid is not None and last_pid != p.pid and context_delay > 0:
                gantt_chart.append(("CS", time, time + context_delay))
                time += context_delay

            p.start_time = time
            p.response_time = time - p.arrival_time
            time += p.burst_time
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

            gantt_chart.append((p.pid, p.start_time, p.completion_time))
            last_pid = p.pid
            is_completed[idx] = True
            completed += 1
        else:
            time += 1

    return gantt_chart
