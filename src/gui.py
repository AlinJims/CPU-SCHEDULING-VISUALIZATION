import random
import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
from scheduler import run_scheduling
from tkinter import filedialog
from PIL import Image, ImageGrab




class SchedulerGUI:
    def export_metrics_csv(self):
        if not hasattr(self, "last_metrics") or not self.last_metrics:
            messagebox.showwarning("No Metrics", "No metrics available to export. Run a simulation first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")],
                                                 title="Save Metrics As")
        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write("PID,Arrival Time,Burst Time,Completion Time,TAT,RT\n")
                for entry in self.last_metrics["details"]:
                    f.write(f"{entry['pid']},{entry['at']},{entry['bt']},{entry['ct']},{entry['tat']},{entry['rt']}\n")
                f.write(f"\nAverage TAT,{self.last_metrics['avg_tat']:.2f}\n")
                f.write(f"Average RT,{self.last_metrics['avg_rt']:.2f}\n")
            messagebox.showinfo("Success", f"Metrics saved as:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save metrics:\n{e}")

    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Visualizer")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
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

        config_frame = ttk.LabelFrame(top_layout, text="Process Configuration", style="DarkLabelFrame.TLabelframe")
        config_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(config_frame, text="Arrival Time:").pack(anchor="w")
        self.arrival_entry = ttk.Entry(config_frame)
        self.arrival_entry.pack(fill="x")

        ttk.Label(config_frame, text="Execution Time:").pack(anchor="w")
        self.burst_entry = ttk.Entry(config_frame)
        self.burst_entry.pack(fill="x")

        btn_frame = ttk.Frame(config_frame)
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="Generate Random", command=self.generate_random_processes,
            bg="#002244" if self.dark_mode else "#ffffff",
            fg="#f0f0f0" if self.dark_mode else "black",
            activebackground="#003366",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Enqueue +", command=self.add_process_row,
            bg="#002244" if self.dark_mode else "#ffffff",
            fg="#f0f0f0" if self.dark_mode else "black",
            activebackground="#003366",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Update", command=self.update_last_process,
            bg="#002244" if self.dark_mode else "#ffffff",
            fg="#f0f0f0" if self.dark_mode else "black",
            activebackground="#003366",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all_processes,
            bg="#002244" if self.dark_mode else "#ffffff",
            fg="#ffffff" if self.dark_mode else "black",
            activebackground="#003366",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat").pack(fill="x", pady=2)

        self.table_frame = ttk.Frame(config_frame)
        self.table_frame.pack(fill="x", pady=10)
        self.add_process_row()

        sim_frame = ttk.LabelFrame(top_layout, text="Simulation", style="DarkLabelFrame.TLabelframe")
        sim_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(sim_frame, text="Choose Algorithm").pack(anchor="w")
        algo_dropdown = ttk.Combobox(sim_frame, textvariable=self.algorithm,
                                     values=["FCFS", "SJF", "SRTF", "RR", "MLFQ"], state="readonly")
        algo_dropdown.pack(fill="x")

        ttk.Label(sim_frame, text="Time Quantum (for RR only):").pack(anchor="w")
        self.quantum_entry = ttk.Entry(sim_frame)
        self.quantum_entry.pack(fill="x", pady=2)

        ttk.Label(sim_frame, text="Context Switch Delay:").pack(anchor="w")
        self.context_entry = ttk.Entry(sim_frame)
        self.context_entry.insert(0, "0")
        self.context_entry.pack(fill="x", pady=2)

        ttk.Button(sim_frame, text="Simulate ▶", command=self.run_scheduling).pack(pady=10)
        ttk.Button(sim_frame, text="Dark Mode", command=self.toggle_dark_mode).pack()
        ttk.Button(sim_frame, text="Export Gantt Chart as PNG", command=self.export_gantt_chart).pack(pady=5)
        ttk.Button(sim_frame, text="Export Metrics as CSV", command=self.export_metrics_csv).pack(pady=5)



       
        self.step_log = tk.Text(sim_frame, height=6, font=("Consolas", 9), wrap="word")
        self.step_log.pack(fill="both", expand=True, pady=5)

        self.result_box = tk.Text(sim_frame, height=8, font=("Consolas", 10), wrap="word")
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
        button_bg = "#002244" if mode == "dark" else "#e0e0e0"
        button_fg = "#f0f0f0" if mode == "dark" else "black"
        hover_bg = "#003366" if mode == "dark" else "#d0d0d0"
    
        self.root.configure(bg=bg)
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TLabelFrame", background=bg, foreground=fg)
        self.style.configure("DarkLabelFrame.TLabelframe", background=bg)
        self.style.configure("DarkLabelFrame.TLabelframe.Label", background=bg, foreground=fg)
        self.style.configure("TCombobox", fieldbackground=bg, foreground=fg)

        self.style.configure("Custom.TButton",
                         background=button_bg,
                         foreground=button_fg,
                         borderwidth=1,
                         focusthickness=3,
                         focuscolor='none',
                         font=("Segoe UI", 10, "bold"))
        self.style.map("Custom.TButton",
                   background=[("active", hover_bg), ("pressed", "#001933")],
                   foreground=[("active", button_fg), ("pressed", button_fg)])

        self.result_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.gantt_canvas.configure(bg=bg)
        self.step_log.configure(bg=bg, fg=fg, insertbackground=fg)

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
        self.step_log.delete(1.0, tk.END)
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
            
        self.last_metrics = None

        global CONTEXT_SWITCH_DELAY
        try:
            CONTEXT_SWITCH_DELAY = int(self.context_entry.get())
            if CONTEXT_SWITCH_DELAY < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Context Switch Delay", "Please enter a non-negative integer.")
            return

        try:
            result = run_scheduling(algo, processes, quantum=quantum, context_delay=CONTEXT_SWITCH_DELAY)
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
        
        self.last_metrics = metrics 


        if gantt and CONTEXT_SWITCH_DELAY > 0:
            new_gantt = []
            last_end = 0
            for i, (pid, start, end) in enumerate(gantt):
                if i > 0 and start > last_end:
                
                    pass
                elif i > 0:
              
                    delay_start = last_end
                    delay_end = last_end + CONTEXT_SWITCH_DELAY
                    new_gantt.append(("-", delay_start, delay_end))
                    start += CONTEXT_SWITCH_DELAY
                    end += CONTEXT_SWITCH_DELAY
                new_gantt.append((pid, start, end))
                last_end = end
            gantt = new_gantt

        if metrics:
            self.result_box.insert(tk.END, "\n=== Metrics ===\n")
            for entry in self.last_metrics.get("details", []):
                self.result_box.insert(tk.END, f"{entry['pid']}: AT={entry['at']} BT={entry['bt']} CT={entry['ct']} "
                                               f"TAT={entry['tat']} RT={entry['rt']}\n")
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
            self.step_log.delete(1.0, tk.END)

        if index >= len(gantt):
            return

        pid, start, end = gantt[index]
        scale = 30
        height = 40
        width = (end - start) * scale

        if pid == "-":
            color = "#cccccc"
            label = "CS"
        else:
            color = f"#{hex(hash(pid) & 0xFFFFFF)[2:]:0>6}"
            label = pid

        self.gantt_canvas.create_rectangle(x, 10, x + width, 10 + height, fill=color, outline="black")
        self.gantt_canvas.create_text(x + width // 2, 30, text=label)

        tick_color = "#f0f0f0" if self.dark_mode else "black"
        self.gantt_canvas.create_text(x, 60, text=str(start), anchor="w", font=("Arial", 9), fill=tick_color)

   
        if index == len(gantt) - 1:
            tick_color = "#f0f0f0" if self.dark_mode else "black"
        self.gantt_canvas.create_text(x + width, 60, text=str(end), anchor="w", font=("Arial", 9), fill=tick_color)

        self.step_log.insert(tk.END, f"At time {start}: {pid} starts\n")
        self.step_log.see(tk.END)

        self.root.after(300, lambda: self.animate_gantt_chart(gantt, index + 1, x + width))

    def export_gantt_chart(self):

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")],
                                                 title="Save Gantt Chart As")
        if not file_path:
            return 

        
        self.root.update() 
        x = self.gantt_canvas.winfo_rootx()
        y = self.gantt_canvas.winfo_rooty()
        x1 = x + self.gantt_canvas.winfo_width()
        y1 = y + self.gantt_canvas.winfo_height()

   
        try:
            img = ImageGrab.grab(bbox=(x, y, x1, y1))
            img.save(file_path)
            messagebox.showinfo("Success", f"Gantt chart saved as:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export image:\n{e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
