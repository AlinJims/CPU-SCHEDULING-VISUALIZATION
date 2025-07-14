def simulate_sjf(processes):
    processes.sort(key=lambda p: (p.arrival_time, p.burst_time))
    time = 0
    completed = 0
    n = len(processes)
    gantt_chart = []
    is_completed = [False] * n

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
            p.start_time = time
            p.response_time = time - p.arrival_time
            time += p.burst_time
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            gantt_chart.append((p.pid, p.start_time, p.completion_time))
            is_completed[idx] = True
            completed += 1
        else:
            time += 1

    return gantt_chart
