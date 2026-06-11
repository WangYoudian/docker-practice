
import os
import time
import math

# CPU stress: 计算平方根
def cpu_stress():
    x = 0.0001
    for _ in range(50_000_000):
        x = math.sqrt(x + 0.0001)

if __name__ == "__main__":
    mode = os.environ.get("STRESS_MODE", "cpu")
    print(f"Stress mode: {mode}, PID: {os.getpid()}")
    if mode == "cpu":
        cpu_stress()
    elif mode == "memory":
        data = []
        while True:
            data.append("x" * 10_000_000)  # 每次追加 10MB
            print(f"Allocated {len(data) * 10}MB")
            time.sleep(0.5)
    elif mode == "idle":
        time.sleep(3600)
    print("Done")
