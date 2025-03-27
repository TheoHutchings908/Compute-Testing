import matplotlib.pyplot as plt

# Data from your tests (update with your actual measurements if needed)
# Total Requests: 2000, 5000, 20000, 30000, 50000
total_requests = [2000, 5000, 20000, 30000, 50000]

# Requests per second (RPS) values from each test
rps_values = [289.08, 295.36, 293.92, 292.37, 285.34]

# Mean time per request (latency) in milliseconds from each test
latency_values = [345.925, 338.573, 340.223, 342.036, 350.453]

# Create the plot with two y-axes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot RPS on the primary y-axis (left)
color = 'tab:blue'
ax1.set_xlabel('Total Requests')
ax1.set_ylabel('Requests per Second (RPS)', color=color)
ax1.plot(total_requests, rps_values, marker='o', linestyle='-', color=color, label='RPS')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title('Performance Metrics vs. Total Requests')

# Create a second y-axis for latency (mean time per request)
ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Mean Time per Request (ms)', color=color)
ax2.plot(total_requests, latency_values, marker='s', linestyle='--', color=color, label='Latency (ms)')
ax2.tick_params(axis='y', labelcolor=color)

# Add a legend by combining both plots
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

plt.tight_layout()
plt.show()
