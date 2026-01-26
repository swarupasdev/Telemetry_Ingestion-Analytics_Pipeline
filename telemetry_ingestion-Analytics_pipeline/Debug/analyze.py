import time
import csv
import os

CSV_FILE = "telemetry.csv"

while True:
    if not os.path.exists(CSV_FILE):
        print("Waiting for telemetry.csv...")
        time.sleep(2)
        continue

    data = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cpu = float(row["cpu"])
                ram = float(row["ram"])
                data.append({"cpu": cpu, "ram": ram})
            except (ValueError, TypeError):
                # Skip header rows or corrupted lines
                continue

    if not data:
        print("No valid data yet...")
        time.sleep(2)
        continue

    cpu_avg = sum(d["cpu"] for d in data) / len(data)
    ram_avg = sum(d["ram"] for d in data) / len(data)

    print("Samples:", len(data))
    print("CPU avg:", round(cpu_avg, 2))
    print("RAM avg:", round(ram_avg, 2))
    print("-" * 30)

    time.sleep(5)
