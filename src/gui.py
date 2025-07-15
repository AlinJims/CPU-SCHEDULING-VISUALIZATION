import random
import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
from scheduler import run_scheduling

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Visualizer")
        self.process_entries = []

        self.algorithm = tk.StringVar()
        self.algorithm.set("FCFS")

        self.setup_ui()

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

            pid_entry.grid(row=i, column=0, padx=5, pady=5)
            at_entry.grid(row=i, column=1, padx=5, pady=5)
            bt_entry.grid(row=i, column=2, padx=5, pady=5)

            self.process_entries.append((pid_entry, at_entry, bt_entry))

    def setup_ui(self):
        algo_label = ttk.Label(self.root, text="Select Algorithm:")
        algo_label.grid(row=0, column=0, padx=10, pady=10)
        algo_menu = ttk.Combobox(self.root, textvariable=self.algorithm, values=["FCFS", "SJF"], state="readonly")
        algo_menu.grid(row=0, column=1, padx=10, pady=10)

        self.table_frame = ttk.LabelFrame(self.root, text="Processes (PID, Arrival Time, Burst Time)")
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.add_process_row()

        add_button = ttk.Button(self.root, text="Add Process", command=self.add_process_row)
        add_button.grid(row=2, column=0, padx=10, pady=10)

        generate_button = ttk.Button(self.root, text="Generate Random", command=self.generate_random_processes)
        generate_button.grid(row=2, column=2, padx=10, pady=10)

        run_button = ttk.Button(self.root, text="Run", command=self.run_scheduling)
        run_button.grid(row=2, column=1, padx=10, pady=10)

        self.result_box = tk.Text(self.root, height=10, width=60)
        self.result_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        canvas_frame = ttk.Frame(self.root)
        canvas_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.canvas_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal")
        self.canvas_scrollbar.pack(side="bottom", fill="x")

        self.gantt_canvas = tk.Canvas(canvas_frame, height=120, bg="white", xscrollcommand=self.canvas_scrollbar.set)
        self.gantt_canvas.pack(side="left", fill="both", expand=True)

        self.canvas_scrollbar.config(command=self.gantt_canvas.xview)

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def add_process_row(self):
        row = len(self.process_entries)
        pid_entry = ttk.Entry(self.table_frame, width=5)
        at_entry = ttk.Entry(self.table_frame, width=10)
        bt_entry = ttk.Entry(self.table_frame, width=10)

        pid_entry.grid(row=row, column=0, padx=5, pady=5)
        at_entry.grid(row=row, column=1, padx=5, pady=5)
        bt_entry.grid(row=row, column=2, padx=5, pady=5)

        self.process_entries.append((pid_entry, at_entry, bt_entry))

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
        try:
            gantt = run_scheduling(algo, processes)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, f"=== {algo} Gantt Chart ===\n")
        for pid, start, end in gantt:
            self.result_box.insert(tk.END, f"{pid}: {start} → {end}\n")

        self.gantt_canvas.delete("all")
        self.animate_gantt_chart(gantt)

    def animate_gantt_chart(self, gantt, index=0, x=10):
        if index == 0:
            self.tick_labels = []
            total_time = gantt[-1][2]
            total_width = total_time * 30
            self.gantt_canvas.config(scrollregion=(0, 0, total_width + 40, 120))

        if index >= len(gantt):
            scale = 30
            height = 40
            for t in range(gantt[-1][2] + 1):
                x_pos = 10 + t * scale
                tick = self.gantt_canvas.create_text(x_pos, 80, text=str(t), font=("Arial", 8))
                self.gantt_canvas.create_line(x_pos, 50, x_pos, 10 + height, fill="gray", dash=(2, 2))
                self.tick_labels.append(tick)
            return

        pid, start, end = gantt[index]
        scale = 30
        height = 40
        width = (end - start) * scale

        self.gantt_canvas.create_rectangle(x, 10, x + width, 10 + height,
                                           fill=f"#{hex(hash(pid) & 0xFFFFFF)[2:]:0>6}", outline="black")
        self.gantt_canvas.create_text(x + width // 2, 30, text=pid)

        self.root.after(700, lambda: self.animate_gantt_chart(gantt, index + 1, x + width))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
