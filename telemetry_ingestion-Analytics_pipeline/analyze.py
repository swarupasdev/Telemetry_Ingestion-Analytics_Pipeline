import time
import csv

def read_csv(filename):
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "cpu": float(row["cpu"]),
                "ram": float(row["ram"]),
                "sensorA": float(row["sensorA"])
            })

    return data


while True:
    try:
        data = read_csv("telemetry.csv")

        if not data:
            print("No data yet...")
            time.sleep(2)
            continue

        cpu_avg = sum(d["cpu"] for d in data) / len(data)
        ram_avg = sum(d["ram"] for d in data) / len(data)
        sensor_max = max(d["sensorA"] for d in data)

        print("Samples:", len(data))
        print("CPU avg:", round(cpu_avg, 2))
        print("RAM avg:", round(ram_avg, 2))
        print("SensorA max:", round(sensor_max, 2))
        print("-" * 30)

        time.sleep(5)

    except FileNotFoundError:
        print("Waiting for telemetry.csv...")
        time.sleep(2)
