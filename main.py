from src.process import Process
from src.fcfs import simulate_fcfs

def print_table(processes):
    print("\nProcess Table:")
    print("PID\tAT\tBT\tCT\tTAT\tWT\tRT")
    total_tat = total_rt = 0
    for p in processes:
        total_tat += p.turnaround_time
        total_rt += p.response_time
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}\t{p.response_time}")
    n = len(processes)
    print(f"\nAverage Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Response Time: {total_rt / n:.2f}")

def print_gantt(gantt_chart):
    print("\nGantt Chart:")
    for pid, start, end in gantt_chart:
        print(f"| P{pid} ", end='')
    print("|")
    for pid, start, end in gantt_chart:
        print(f"{start:<5}", end='')
    print(f"{gantt_chart[-1][2]}")

def main():
    print("CPU Scheduling Simulator - FCFS")
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        at = int(input(f"Arrival time for P{i}: "))
        bt = int(input(f"Burst time for P{i}: "))
        processes.append(Process(i, at, bt))

    gantt_chart = simulate_fcfs(processes)
    print_gantt(gantt_chart)
    print_table(processes)

if __name__ == "__main__":
    main()
