import subprocess
import time
process = [None] * 100
start_time = time.time()
for i in range(5):
    time.sleep(0.1)
    # Create and launch process pop.py using python interpreter
    process[i] = subprocess.Popen(["python3", "testclient.py"])

for i in range(5):
    # Wait for process to terminate
    process[i].wait()
print(time.time()-start_time)
