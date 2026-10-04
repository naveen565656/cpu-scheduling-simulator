import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="💻",
    layout="wide"
)

st.title("💻 CPU Scheduling Simulator")
st.write("Visualize CPU scheduling algorithms")

st.sidebar.header("Simulation Settings")

algorithm = st.sidebar.selectbox(
    "Select Scheduling Algorithm",
    ["FCFS", "SJF"]
)

st.subheader("Process Details")

num = st.number_input(
    "Number of Processes",
    min_value=1,
    max_value=10,
    value=4
)

processes = []

for i in range(int(num)):
    st.write(f"Process P{i+1}")

    col1, col2 = st.columns(2)

    with col1:
        arrival = st.number_input(
            f"Arrival Time P{i+1}",
            min_value=0,
            value=0,
            key=f"a{i}"
        )

    with col2:
        burst = st.number_input(
            f"Burst Time P{i+1}",
            min_value=1,
            value=5,
            key=f"b{i}"
        )

    processes.append({
        "id": f"P{i+1}",
        "arrival": arrival,
        "burst": burst
    })

if st.button("Run Simulation"):

    if algorithm == "FCFS":
        processes.sort(key=lambda p: (p["arrival"], p["id"]))

    else:
        processes.sort(key=lambda p: (p["arrival"], p["burst"], p["id"]))

    current_time = 0
    results = []
    gantt = []

    while processes:
        available = [
            p for p in processes
            if p["arrival"] <= current_time
        ]

        if not available:
            current_time = min(p["arrival"] for p in processes)
            continue

        if algorithm == "FCFS":
            p = min(available, key=lambda x: (x["arrival"], x["id"]))
        else:
            p = min(available, key=lambda x: (x["burst"], x["arrival"], x["id"]))

        processes.remove(p)

        start = current_time
        completion = start + p["burst"]

        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "Process": p["id"],
            "Arrival Time": p["arrival"],
            "Burst Time": p["burst"],
            "Completion Time": completion,
            "Waiting Time": waiting,
            "Turnaround Time": turnaround
        })

        gantt.append((p["id"], start, completion))
        current_time = completion

    st.subheader("Scheduling Results")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    avg_waiting = df["Waiting Time"].mean()
    avg_turnaround = df["Turnaround Time"].mean()

    col1, col2 = st.columns(2)

    col1.metric("Average Waiting Time", f"{avg_waiting:.2f}")
    col2.metric("Average Turnaround Time", f"{avg_turnaround:.2f}")

    st.subheader("Gantt Chart")

    fig, ax = plt.subplots(figsize=(10, 2))

    for pid, start, end in gantt:
        ax.barh(
            0,
            end - start,
            left=start,
            height=0.5,
            edgecolor="black"
        )

        ax.text(
            (start + end) / 2,
            0,
            pid,
            ha="center",
            va="center"
        )

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(f"{algorithm} Scheduling")
    ax.set_xticks(sorted(set([0] + [x[2] for x in gantt])))
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)