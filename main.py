import random
from src.process import Process
from src.fcfs import fcfs_scheduling
from src.sjf import sjf_scheduling
from src.srtf import srtf_scheduling
from src.rr import rr_scheduling
from src.mlfq import mlfq_scheduling

def print_gantt_chart(gantt):
    print("\nGantt Chart:")
    timeline = "|"
    timestamps = ""
    for pid, start, end in gantt:
        timeline += f" {pid} |"
        timestamps += f"{start:<5}"
    timestamps += f"{gantt[-1][2]}"
    print(timeline)
    print(timestamps)

def print_table(metrics):
    print("\nProcess Table:")
    print("PID\tAT\tBT\tCT\tTAT\tRT")
    for p in metrics["details"]:
        print(f"{p['pid']}\t{p['at']}\t{p['bt']}\t{p['ct']}\t{p['tat']}\t{p['rt']}")
    print(f"\nAverage Turnaround Time: {metrics['avg_tat']:.2f}")
    print(f"Average Response Time: {metrics['avg_rt']:.2f}")

def get_manual_input():
    processes = []
    n = int(input("Enter number of processes: "))
    for i in range(n):
        pid = f"P{i+1}"
        at = int(input(f"Arrival time for {pid}: "))
        bt = int(input(f"Burst time for {pid}: "))
        processes.append(Process(pid, at, bt))
    return processes

def get_random_processes():
    processes = []
    n = int(input("Enter number of processes to generate: "))
    for i in range(n):
        pid = f"P{i+1}"
        at = random.randint(0, 10)
        bt = random.randint(1, 10)
        processes.append(Process(pid, at, bt))
    print("Randomly generated processes:")
    for p in processes:
        print(f"{p.pid}: Arrival={p.arrival_time}, Burst={p.burst_time}")
    return processes

def main():
    print("\nWelcome to CPU Scheduling Visualizer (Terminal Mode)")
    print("1. Manual Input")
    print("2. Randomly Generate Processes")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        processes = get_manual_input()
    elif choice == '2':
        processes = get_random_processes()
    else:
        print("Invalid choice.")
        return

    print("\nChoose Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF")
    print("3. SRTF")
    print("4. Round Robin (RR)")
    print("5. Multilevel Feedback Queue (MLFQ)")
    algo_choice = input("Enter choice [1-5]: ")

    quantum = None
    if algo_choice == '4':
        quantum = int(input("Enter time quantum for Round Robin: "))
    elif algo_choice == '5':
        print("Using default MLFQ quantums and allotments.\n")

    if algo_choice == '1':
        gantt, metrics = fcfs_scheduling(processes), None
    elif algo_choice == '2':
        gantt, metrics = sjf_scheduling(processes), None
    elif algo_choice == '3':
        gantt, metrics = srtf_scheduling(processes)
    elif algo_choice == '4':
        gantt, metrics = rr_scheduling(processes, quantum)
    elif algo_choice == '5':
        gantt, metrics = mlfq_scheduling(processes)
    else:
        print("Invalid algorithm choice.")
        return

    print_gantt_chart(gantt)

    if metrics:
        print_table(metrics)

if __name__ == "__main__":
    main()
