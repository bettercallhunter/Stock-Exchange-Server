import matplotlib.pyplot as plt
import numpy as np
# Sample data
x_values = [1, 2, 3, 4]
y_values = [419.07, 835.61, 1022.30, 1021.55]
y_errors = [40.45, 71.90, 64.50, 59.24]

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the data with error bars
ax.bar(x_values, y_values, yerr=y_errors, capsize=5, width=0.5)
# Set the x-axis ticks
ax.set_xticks([1, 2, 3, 4])
# Set axis labels and title
ax.set_xlabel('core number')
ax.set_ylabel('throughput(request/s)')
ax.set_title('Scalability')
plt.savefig('scalability.png')
# Display the graph
plt.show()
