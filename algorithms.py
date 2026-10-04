
def fcfs(processes):
    processes = sorted(
        processes,
        key=lambda p: (p["arrival"], p["id"])
    )

    current_time = 0
    results = []
    gantt = []

    for p in processes:
        pid = p["id"]
        arrival = p["arrival"]
        burst = p["burst"]

        start = max(current_time, arrival)
        completion = start + burst

        turnaround = completion - arrival
        waiting = turnaround - burst

        results.append({
            "id": pid,
            "arrival": arrival,
            "burst": burst,
            "start": start,
            "completion": completion,
            "turnaround": turnaround,
            "waiting": waiting
        })

        gantt.append((pid, start, completion))
        current_time = completion

    return results, gantt
