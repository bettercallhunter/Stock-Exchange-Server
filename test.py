import subprocess
import time
process = [None] * 1000
for i in range(1000):
    start_time = time.time()
    # Create and launch process pop.py using python interpreter
    process[i] = subprocess.Popen(["python3", "testclient.py"])

for i in range(1000):
    # Wait for process to terminate
    process[i].wait()
print(time.time()-start_time)
