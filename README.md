🧠 CPU Scheduling Simulator (Streamlit Web App)
📌 Overview
The CPU Scheduling Simulator is a web-based application built using Python and Streamlit. It provides an intuitive interface to simulate and visualize various CPU scheduling algorithms. Users can input custom process data, select scheduling algorithms, and view results including average waiting time, turnaround time, and a Gantt chart. This tool is designed for learning, experimentation, and understanding how different CPU scheduling strategies work in real-time.

🎯 Project Objectives
Simulate key CPU scheduling algorithms with user-defined input.

Provide interactive visual feedback through tables and Gantt charts.

Calculate and display important process metrics.

Help students, developers, and learners understand scheduling logic.

🧮 Supported Scheduling Algorithms
First Come First Serve (FCFS) – Non-preemptive

Shortest Job First (SJF) – Non-preemptive

Round Robin (RR) – Preemptive with time quantum

Priority Scheduling – Non-preemptive with priority input

Shortest Remaining Time First (SRTF) – Preemptive

Multi-Level Queue (MLQ) – Non-preemptive (based on priority levels)

⚙️ Features
Select from 6 popular scheduling algorithms.

Input number of processes and specify:

Arrival Time

Burst Time

Priority (if applicable)

Round Robin supports custom time quantum.

Displays a detailed results table:

Completion Time

Turnaround Time

Waiting Time

Computes and shows:

Average Waiting Time

Average Turnaround Time

Generates a dynamic Gantt Chart for visual process scheduling.

💡 Technologies Used
Python 3

Streamlit – UI framework for interactive web apps

Pandas – Data handling and tabulation

Matplotlib – Gantt chart visualization

