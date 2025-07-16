import random
import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
from scheduler import run_scheduling

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Visualizer")
        self.root.geometry("1100x700")
        self.process_entries = []
        self.algorithm = tk.StringVar(value="FCFS")
        self.dark_mode = False

        self.style = ttk.Style()

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        header = ttk.Label(self.main_frame, text="CPU Scheduling Visualizer", font=("Segoe UI", 18, "bold"))
        header.pack(pady=10)

        top_layout = ttk.Frame(self.main_frame)
        top_layout.pack(fill="x", padx=10, pady=10)

        config_frame = ttk.LabelFrame(top_layout, text="Process Configuration")
        config_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(config_frame, text="Arrival Time:").pack(anchor="w")
        self.arrival_entry = ttk.Entry(config_frame)
        self.arrival_entry.pack(fill="x")

        ttk.Label(config_frame, text="Execution Time:").pack(anchor="w")
        self.burst_entry = ttk.Entry(config_frame)
        self.burst_entry.pack(fill="x")

        btn_frame = ttk.Frame(config_frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Generate Random", command=self.generate_random_processes).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Enqueue +", command=self.add_process_row).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Update", command=self.update_last_process).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all_processes).pack(fill="x", pady=2)

        self.table_frame = ttk.Frame(config_frame)
        self.table_frame.pack(fill="x", pady=10)
        self.add_process_row()

        sim_frame = ttk.LabelFrame(top_layout, text="Simulation")
        sim_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(sim_frame, text="Choose Algorithm (FCFS, SJF, SRTF)").pack(anchor="w")
        algo_dropdown = ttk.Combobox(sim_frame, textvariable=self.algorithm, values=["FCFS", "SJF", "SRTF", "RR", "MLFQ"], state="readonly")
        algo_dropdown.pack(fill="x")

        ttk.Label(sim_frame, text="Time Quantum (for RR only):").pack(anchor="w")
        self.quantum_entry = ttk.Entry(sim_frame)
        self.quantum_entry.pack(fill="x", pady=2)

        ttk.Button(sim_frame, text="Simulate ▶", command=self.run_scheduling).pack(pady=10)
        ttk.Button(sim_frame, text="Dark Mode", command=self.toggle_dark_mode).pack()

        self.result_box = tk.Text(sim_frame, height=12, font=("Consolas", 10), wrap="word")
        self.result_box.pack(fill="both", expand=True, pady=5)

        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="horizontal")
        self.canvas_scrollbar.pack(side="bottom", fill="x")

        self.gantt_canvas = tk.Canvas(self.canvas_frame, height=140, bg="white", xscrollcommand=self.canvas_scrollbar.set)
        self.gantt_canvas.pack(side="left", fill="both", expand=True)
        self.canvas_scrollbar.config(command=self.gantt_canvas.xview)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_theme("dark" if self.dark_mode else "light")

    def set_theme(self, mode):
        bg = "#1e1e1e" if mode == "dark" else "white"
        fg = "#f0f0f0" if mode == "dark" else "black"
        self.root.configure(bg=bg)
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TLabelFrame", background=bg, foreground=fg)
        self.style.configure("TButton", background=bg, foreground=fg)
        self.style.configure("TCombobox", fieldbackground=bg, foreground=fg)
        self.result_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.gantt_canvas.configure(bg=bg)

    def add_process_row(self):
        row = len(self.process_entries)
        pid_entry = ttk.Entry(self.table_frame, width=5)
        at_entry = ttk.Entry(self.table_frame, width=10)
        bt_entry = ttk.Entry(self.table_frame, width=10)
        pid_entry.grid(row=row, column=0, padx=5, pady=2)
        at_entry.grid(row=row, column=1, padx=5, pady=2)
        bt_entry.grid(row=row, column=2, padx=5, pady=2)
        self.process_entries.append((pid_entry, at_entry, bt_entry))

    def generate_random_processes(self, count=5):
        for widgets in self.table_frame.winfo_children():
            widgets.destroy()
        self.process_entries.clear()
        for i in range(count):
            pid_entry = ttk.Entry(self.table_frame, width=5)
            at_entry = ttk.Entry(self.table_frame, width=10)
            bt_entry = ttk.Entry(self.table_frame, width=10)
            pid = f"P{i+1}"
            arrival = random.randint(0, 10)
            burst = random.randint(1, 10)
            pid_entry.insert(0, pid)
            at_entry.insert(0, str(arrival))
            bt_entry.insert(0, str(burst))
            pid_entry.grid(row=i, column=0, padx=5, pady=2)
            at_entry.grid(row=i, column=1, padx=5, pady=2)
            bt_entry.grid(row=i, column=2, padx=5, pady=2)
            self.process_entries.append((pid_entry, at_entry, bt_entry))

    def update_last_process(self):
        if not self.process_entries:
            self.add_process_row()

        pid = f"P{len(self.process_entries)}"
        arrival = self.arrival_entry.get()
        burst = self.burst_entry.get()

        last_row = self.process_entries[-1]
        last_row[0].delete(0, tk.END)
        last_row[0].insert(0, pid)
        last_row[1].delete(0, tk.END)
        last_row[1].insert(0, arrival)
        last_row[2].delete(0, tk.END)
        last_row[2].insert(0, burst)

    def clear_all_processes(self):
        for entry in self.process_entries:
            for widget in entry:
                widget.destroy()
        self.process_entries.clear()
        self.result_box.delete(1.0, tk.END)
        self.gantt_canvas.delete("all")

    def run_scheduling(self):
        processes = []
        for entry in self.process_entries:
            try:
                pid = entry[0].get()
                arrival = int(entry[1].get())
                burst = int(entry[2].get())
                processes.append(Process(pid, arrival, burst))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integers for arrival and burst times.")
                return

        algo = self.algorithm.get()
        quantum = None
        if algo == "RR":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Quantum", "Please enter a valid positive integer for time quantum.")
                return

        try:
            result = run_scheduling(algo, processes, quantum)
            if isinstance(result, tuple) and len(result) == 2:
                gantt, metrics = result
            else:
                gantt = result
                metrics = None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, f"=== {algo} Gantt Chart ===\n")
        for pid, start, end in gantt:
            self.result_box.insert(tk.END, f"{pid}: {start} → {end}\n")

        if metrics:
            self.result_box.insert(tk.END, "\n=== Metrics ===\n")
            for entry in metrics["details"]:
                self.result_box.insert(tk.END, f"{entry['pid']}: AT={entry['at']} BT={entry['bt']} CT={entry['ct']} TAT={entry['tat']} RT={entry['rt']}\n")
            self.result_box.insert(tk.END, f"\nAverage TAT: {metrics['avg_tat']:.2f}")
            self.result_box.insert(tk.END, f"\nAverage RT: {metrics['avg_rt']:.2f}")

        self.gantt_canvas.delete("all")
        self.animate_gantt_chart(gantt)


    def animate_gantt_chart(self, gantt, index=0, x=10):
        if not gantt:
            return
        if index == 0:
            self.tick_labels = []
            total_time = gantt[-1][2]
            total_width = total_time * 30
            self.gantt_canvas.config(scrollregion=(0, 0, total_width + 40, 140))

        if index >= len(gantt):
            scale = 30
            height = 40
            for t in range(gantt[-1][2] + 1):
                x_pos = 10 + t * scale
                tick = self.gantt_canvas.create_text(x_pos, 90, text=str(t), font=("Arial", 8))
                self.gantt_canvas.create_line(x_pos, 50, x_pos, 50 + height, fill="gray", dash=(2, 2))
                self.tick_labels.append(tick)
            return

        pid, start, end = gantt[index]
        scale = 30
        height = 40
        width = (end - start) * scale
        self.gantt_canvas.create_rectangle(x, 10, x + width, 10 + height,
                                           fill=f"#{hex(hash(pid) & 0xFFFFFF)[2:]:0>6}", outline="black")
        self.gantt_canvas.create_text(x + width // 2, 30, text=pid)
        self.root.after(300, lambda: self.animate_gantt_chart(gantt, index + 1, x + width))


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
