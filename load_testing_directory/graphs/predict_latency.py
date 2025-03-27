import matplotlib.pyplot as plt
import numpy as np

# Measured data points (example values)
#  - At 1,000 requests, the mean latency is 347 ms.
#  - At 10,000 requests, the mean latency is 1736 ms.
requests_data = np.array([1000, 10000])
latency_data = np.array([347, 1736])

# Fit a linear model to the data points
coeffs = np.polyfit(requests_data, latency_data, 1)
model = np.poly1d(coeffs)
print("Linear model: latency = {:.2f} * requests + {:.2f}".format(coeffs[0], coeffs[1]))

# Predict latency for a range of request quantities (e.g., from 1,000 to 50,000)
x_vals = np.linspace(1000, 50000, 100)
y_vals = model(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="Predicted Mean Latency", color="blue")
plt.scatter(requests_data, latency_data, color='red', label="Measured Data")
plt.xlabel("Number of Requests")
plt.ylabel("Mean Latency (ms)")
plt.title("Predicted Mean Latency for Larger Request Quantities")
plt.legend()
plt.grid(True)
plt.show()