import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy
import io

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        current_time += process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

def sjf(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')

        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    idx = i
                elif processes[i].burst_time == min_burst:
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            p = processes[idx]
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1

def round_robin(processes, quantum):
    n = len(processes)
    queue = []
    current_time = 0
    completed = 0
    arrived = [False] * n

    while completed != n:
        for i, p in enumerate(processes):
            if p.arrival_time <= current_time and not arrived[i] and p.remaining_time > 0:
                queue.append(p)
                arrived[i] = True

        if not queue:
            current_time += 1
            continue

        process = queue.pop(0)

        if process.remaining_time > quantum:
            current_time += quantum
            process.remaining_time -= quantum
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed += 1

        for i, p in enumerate(processes):
            if p.arrival_time <= current_time and not arrived[i] and p.remaining_time > 0:
                queue.append(p)
                arrived[i] = True

        if process.remaining_time > 0:
            queue.append(process)

def priority_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    current_time = 0
    completed = 0
    n = len(processes)
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_priority = float('inf')

        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].priority < min_priority:
                    min_priority = processes[i].priority
                    idx = i
                elif processes[i].priority == min_priority:
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            p = processes[idx]
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1

def srtf(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    remaining_times = [p.burst_time for p in processes]
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_remaining = float('inf')

        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if remaining_times[i] < min_remaining:
                    min_remaining = remaining_times[i]
                    idx = i

        if idx != -1:
            remaining_times[idx] -= 1
            current_time += 1

            if remaining_times[idx] == 0:
                p = processes[idx]
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                is_completed[idx] = True
                completed += 1
        else:
            current_time += 1

def mlq(processes):
    high_priority_queue = []
    low_priority_queue = []
    current_time = 0
    completed = 0
    processes_sorted = sorted(processes, key=lambda p: p.arrival_time)

    for p in processes_sorted:
        if p.priority < 2:
            high_priority_queue.append(p)
        else:
            low_priority_queue.append(p)

    while completed < len(processes):
        if high_priority_queue:
            p = high_priority_queue.pop(0)
        elif low_priority_queue:
            p = low_priority_queue.pop(0)
        else:
            current_time += 1
            continue

        if current_time < p.arrival_time:
            current_time = p.arrival_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        completed += 1

def plot_gantt_chart(processes):
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 1)
    gnt.set_xlim(0, max(p.completion_time for p in processes) + 1)
    gnt.set_xlabel('Time')
    gnt.set_yticks([])

    for p in processes:
        gnt.broken_barh([(p.arrival_time, p.burst_time)], (0, 1), facecolors=('orange'), edgecolor='black')
        plt.text(p.completion_time - p.burst_time / 2, 0.5, p.pid, ha='center', va='center')

    plt.title('Gantt Chart')
    st.pyplot(fig)  # Use Streamlit to display the figure

# --- STREAMLIT UI ---
st.title("🧠 CPU Scheduling Simulator")

algo = st.selectbox("Choose Scheduling Algorithm", 
                    ["FCFS", "SJF", "Round Robin", "Priority", "SRTF", "MLQ"])

num = st.number_input("Number of Processes", min_value=1, max_value=10, step=1)

quantum = None
if algo == "Round Robin":
    quantum = st.number_input("Time Quantum", min_value=1, step=1)

process_data = []
st.subheader("📝 Enter Process Details")
for i in range(num):
    with st.expander(f"Process {i+1}"):
        pid = f"P{i+1}"
        at = st.number_input(f"Arrival Time of {pid}", key=f"at_{i}", min_value=0, value=i)
        bt = st.number_input(f"Burst Time of {pid}", key=f"bt_{i}", min_value=1, value=5)
        pr = st.number_input(f"Priority of {pid}", key=f"pr_{i}", min_value=0) if algo in ["Priority", "MLQ"] else 0
        process_data.append(Process(pid, at, bt, pr))

if st.button("Run Scheduling"):
    # Deep copy to avoid modifying inputs
    processes = copy.deepcopy(process_data)

    if algo == "FCFS":
        fcfs(processes)
    elif algo == "SJF":
        sjf(processes)
    elif algo == "Round Robin":
        round_robin(processes, quantum)
    elif algo == "Priority":
        priority_scheduling(processes)
    elif algo == "SRTF":
        srtf(processes)
    elif algo == "MLQ":
        mlq(processes)

    df = pd.DataFrame([{
        "PID": p.pid,
        "Arrival Time": p.arrival_time,
        "Burst Time": p.burst_time,
        "Priority": p.priority,
        "Completion Time": p.completion_time,
        "Turnaround Time": p.turnaround_time,
        "Waiting Time": p.waiting_time
    } for p in processes])
    
    st.subheader("📊 Results")
    st.dataframe(df)

    avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)
    st.write(f"*Average Waiting Time*: {avg_waiting:.2f}")
    st.write(f"*Average Turnaround Time*: {avg_turnaround:.2f}")

    # Plot Gantt Chart
    st.subheader("📈 Gantt Chart")
    plot_gantt_chart(processes)

    # Save results as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name='scheduling_results.csv',
        mime='text/csv'
    )
