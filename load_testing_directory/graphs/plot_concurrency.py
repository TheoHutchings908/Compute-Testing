import matplotlib.pyplot as plt

# Sample data from your concurrency increment tests
# Replace these sample values with your actual measurements.
concurrency_levels = [10, 50, 100, 200, 500]
# Example: Requests per second at each concurrency level
rps_values = [1500, 2800, 2880, 2750, 2500]
# Example: Mean latency in milliseconds at each concurrency level
latency_values = [20, 35, 50, 100, 250]

# Create a figure with two subplots (one for RPS and one for latency)
fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot Requests per Second
ax[0].plot(concurrency_levels, rps_values, marker='o', color='blue', linestyle='-')
ax[0].set_title("Performance vs. Concurrency")
ax[0].set_ylabel("Requests per Second (RPS)")
ax[0].grid(True)

# Plot Mean Latency
ax[1].plot(concurrency_levels, latency_values, marker='o', color='red', linestyle='-')
ax[1].set_title("Latency vs. Concurrency")
ax[1].set_xlabel("Concurrency Level")
ax[1].set_ylabel("Mean Latency (ms)")
ax[1].grid(True)

# Adjust layout and display the plot
plt.tight_layout()
plt.show()