<h2 align="center">🖥️ CPU Scheduling Visualization</h2>

<p align="center">
  This is our program that simulates how CPU Scheduling Algorithms
First-In First-Out(FCFS), Shortest Job First(SJF), 
Shortest Remaining Time First(SRTF), Round Robin, and 
Multilevel Feedback Queue(MLFQ) works. This programs lets you simulate and give a visualization of the order process, completion lines, and compute the scheduling metrics.
</p>

## 📘 About The Project

This program simulates how CPU Scheduling Algorithms work:

- **First-In First-Out (FCFS)**  
  Processes are executed strictly in the order they arrive, like a queue. It’s simple but can cause long wait times if a long process arrives first.

- **Shortest Job First (SJF)**  
  The process with the shortest total execution time is run first. It’s non-preemptive, so once a process starts, it runs until finished, minimizing average waiting time.

- **Shortest Remaining Time First (SRTF)**  
  A preemptive version of SJF. If a new process arrives with less remaining time than the current process, it interrupts and runs the new process, always choosing the shortest time left.

- **Round Robin (RR)**  
  Each process gets an equal, fixed time slice (quantum) to run in cyclic order. It’s fair and good for time-sharing systems but can have higher turnaround time.

- **Multilevel Feedback Queue (MLFQ)**  
  Processes are placed in multiple priority queues. They can move between queues based on their execution history and behavior, allowing flexible and dynamic scheduling.

It allows users to:
- Enter custom processes
- Visualize the Gantt chart dynamically
- Compute turnaround & waiting time
- Export results via screenshot

## 🛠️ Built With

- [Python 3](https://www.python.org/)
- [Tkinter GUI](https://docs.python.org/3/library/tkinter.html)
- [Pillow](https://python-pillow.org/)

## 📁 Directory Layout

```
CPU-SCHEDULING-VISUALIZATION/
├── src/
│   └── Contains GUI, Algorithm Scheduling Logic and Predefined Process files
├── main.py
│   └── Project's entry point when launching via terminal. Serves as the central launcher ensuring clear startup
└── test_scheduler.py
    └── For testing and validating CPU Scheduling logic
```

## 🚀 Getting Started

### 📋 Prerequisites

Ensure you have Python 3 installed on your system. Then install the required dependencies:

```bash
pip install pillow
```

### 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your_username/CPU-SCHEDULING-VISUALIZATION.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd CPU-SCHEDULING-VISUALIZATION
   ```

3. **Run the program**
   
   You can run the program using either of the two files:
   
   **Option 1: Run with `gui.py` (directly opens the interface)**
   ```bash
   python src/gui.py
   ```
   
   **Option 2: Run with `main.py` (acts as the main entry point)**
   ```bash
   python main.py
   ```
## 🖼️ Screenshots

### Main Application Interface
![Main Interface](docs/images/maininterface.png)
*The main window showing process input fields and algorithm selection*

## 📊 Sample Input and Output

### Sample Input Data

Here's an example of process data you can input into the system:

| Process ID | Arrival Time | Burst Time | Priority |
|------------|--------------|------------|----------|
| P1         | 0            | 8          | —        |
| P2         | 1            | 4          | —        |
| P3         | 2            | 9          | —        |
| P4         | 3            | 5          | —        |

### Expected Output Examples

#### FCFS (First-Come, First-Served)
![FCFS Gantt Chart](docs/images/fcfs.png)
*Gantt chart showing First-Come, First-Served scheduling*

#### SJF (Shortest Job First)
![FCFS Gantt Chart](docs/images/sjf.png)
*Gantt chart showing Shortest Job First*

#### SRTF (Shortest Remaining Time First)
![FCFS Gantt Chart](docs/images/srtf.png)
*Gantt chart showing Shortest Remaining Time First scheduling*

#### RR (Round Robin) - 3 Time Quantum
![FCFS Gantt Chart](docs/images/rr.png)
*Gantt chart showing Round Robin scheduling*

#### MLFQ (Multi-Level Feedback Queue) - 2, 4, 6, FCFS 
![FCFS Gantt Chart](docs/images/mlfq.png)
*Gantt chart showing Multi-Level Feedback Queue scheduling*

## 👥 Partners

* **Villarte, Adrian** – `josa37`
* **Ybañez, Allain James** – `josa38`

**🔗 GitHub Repo:** [https://github.com/AlinJims/CPU-SCHEDULING-VISUALIZATION.git](https://github.com/your_username/CPU-SCHEDULING-VISUALIZATION)

## 🙌 Acknowledgments

* [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
* [Pillow Documentation](https://python-pillow.org/)
* [GeeksforGeeks CPU Scheduling](https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/)
* [Simple Snippets CPU Scheduling Tutorials](https://www.youtube.com/watch?v=AiVKIdGheEU&list=PLIY8eNdw5tW_lHyageTADFKBt9weJXndE)
* Inspired by OS coursework and CPU scheduling theory by Sir Bayocot

