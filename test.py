from algorithms import fcfs

processes = [
    {"id": "P1", "arrival": 0, "burst": 5},
    {"id": "P2", "arrival": 1, "burst": 3},
    {"id": "P3", "arrival": 2, "burst": 8},
    {"id": "P4", "arrival": 3, "burst": 2}
]

results, gantt = fcfs(processes)

print("CPU Scheduling Results")

for p in results:
    print(
        p["id"],
        "Waiting Time:", p["waiting"],
        "Turnaround Time:", p["turnaround"]
    )

print("Gantt Chart:", gantt)

avg_waiting = sum(p["waiting"] for p in results) / len(results)
avg_turnaround = sum(p["turnaround"] for p in results) / len(results)

print("Average Waiting Time:", avg_waiting)
print("Average Turnaround Time:", avg_turnaround)


