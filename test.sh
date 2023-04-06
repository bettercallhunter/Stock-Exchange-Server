#!/bin/bash

start=$(date +%s.%N)

for i in {1..1000}
do
  python3 testclient.py
done

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc)

echo "Total time to run testclient.py 1000 times: $runtime seconds"
