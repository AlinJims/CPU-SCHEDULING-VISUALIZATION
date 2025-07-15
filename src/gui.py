import tkinter as tk
from tkinter import ttk, messagebox
from process import Process  # Import your Process class

# === Global Process List ===
process_list = []

def add_process():
    pid = entry_pid.get()
    try:
        arrival = int(entry_arrival.get())
        burst = int(entry_burst.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Arrival and Burst time must be integers.")
        return

    if not pid:
        messagebox.showerror("Missing PID", "Please enter a Process ID.")
        return

    process = Process(pid, arrival, burst)
    process_list.append(process)

    update_process_display()

    # Clear inputs
    entry_pid.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)

def update_process_display():
    text_output.delete("1.0", tk.END)
    for p in process_list:
        text_output.insert(tk.END, f"{p.pid} (AT={p.arrival_time}, BT={p.burst_time})\n")

# === Run Simulation Placeholder ===
def run_simulation():
    selected_algo = algo_var.get()
    if not process_list:
        messagebox.showwarning("No Processes", "Please add at least one process.")
        return

    # Create a copy of the process list so original is not mutated
    processes = [Process(p.pid, p.arrival_time, p.burst_time) for p in process_list]

    if selected_algo == "FCFS":
        from src.fcfs import simulate_fcfs
        result = simulate_fcfs(processes)
    elif selected_algo == "SJF":
        from src.sjf import simulate_sjf
        result = simulate_sjf(processes)
    else:
        messagebox.showerror("Unsupported", f"{selected_algo} not implemented.")
        return

    # Display Gantt Chart
    text_output.insert(tk.END, "\n=== Gantt Chart ===\n")
    for pid, start, end in result:
        text_output.insert(tk.END, f"{pid}: {start} → {end}\n")


# === Main Window ===
root = tk.Tk()
root.title("CPU Scheduling Visualizer")
root.geometry("450x400")

# Title
tk.Label(root, text="CPU Scheduling Visualization", font=("Arial", 16)).pack(pady=10)

# Algorithm Dropdown
algo_var = tk.StringVar()
tk.Label(root, text="Select Scheduling Algorithm:").pack()
algo_dropdown = ttk.Combobox(root, textvariable=algo_var, state="readonly")
algo_dropdown['values'] = ("FCFS", "SJF")
algo_dropdown.current(0)
algo_dropdown.pack(pady=5)

# Input Fields Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="PID:").grid(row=0, column=0)
entry_pid = tk.Entry(input_frame, width=10)
entry_pid.grid(row=0, column=1)

tk.Label(input_frame, text="Arrival:").grid(row=0, column=2)
entry_arrival = tk.Entry(input_frame, width=10)
entry_arrival.grid(row=0, column=3)

tk.Label(input_frame, text="Burst:").grid(row=0, column=4)
entry_burst = tk.Entry(input_frame, width=10)
entry_burst.grid(row=0, column=5)

# Add Button
tk.Button(root, text="Add Process", command=add_process).pack(pady=5)

# Process Display
text_output = tk.Text(root, height=10, width=50)
text_output.pack(pady=10)

# Run Button
tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=5)

root.mainloop()
