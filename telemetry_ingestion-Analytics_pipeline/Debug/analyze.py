import time
import csv
import os

CSV_FILE = "telemetry.csv"

CPU_THRESHOLD = 80.0
RAM_THRESHOLD = 80.0

def read_data():
    data = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cpu = float(row["cpu"])
                ram = float(row["ram"])
                data.append({
                    "cpu": cpu,
                    "ram": ram
                })
            except (ValueError, TypeError, KeyError):
                # Skip headers or corrupted rows
                continue

    return data


while True:
    if not os.path.exists(CSV_FILE):
        print("Waiting for telemetry.csv...")
        time.sleep(2)
        continue

    data = read_data()

    if not data:
        print("No valid data yet...")
        time.sleep(2)
        continue

    cpu_avg = sum(d["cpu"] for d in data) / len(data)
    ram_avg = sum(d["ram"] for d in data) / len(data)

    latest = data[-1]

    print("Samples:", len(data))
    print("CPU avg:", round(cpu_avg, 2))
    print("RAM avg:", round(ram_avg, 2))

    if latest["cpu"] > CPU_THRESHOLD:
        print("⚠️  CPU anomaly detected:", round(latest["cpu"], 2))

    if latest["ram"] > RAM_THRESHOLD:
        print("⚠️  RAM anomaly detected:", round(latest["ram"], 2))

    print("-" * 40)
    time.sleep(5)
