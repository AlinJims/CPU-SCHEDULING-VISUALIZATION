# fcfs.py

def fcfs_scheduling(processes, context_delay=0):
    processes.sort(key=lambda p: p.arrival_time)
    time = 0
    gantt_chart = []

    for i, p in enumerate(processes):
        if time < p.arrival_time:
            time = p.arrival_time

        if i > 0 and context_delay > 0:
           
            gantt_chart.append(("CS", time, time + context_delay))
            time += context_delay

        p.start_time = time
        p.response_time = time - p.arrival_time
        time += p.burst_time
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        gantt_chart.append((p.pid, p.start_time, p.completion_time))
    
    return gantt_chart
