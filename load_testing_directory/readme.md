# Load Testing Project

*This directory explores different tests that can be performed to measure load capacity.*

**Author:** Theo Hutchings

---

## Overview

This project implements various load testing strategies to evaluate the performance and stability of our compute service. We utilize both Apache Bench (ab) for quick, command-line based tests and custom Python scripts for more flexible, detailed testing scenarios.

---

## Contents

Firstly you will get a run-through of all the code I have used throughout the testing and what it does. You will then get a summary of the results and a conclusion. I have also written a brief overview of Kubernetes and why we would need to utilize it for running high traffic servers.

---

## Apache Bench (ab) Tests

Apache Bench is a lightweight command-line tool used to benchmark your HTTP server.

### Baseline GET Request- <p>
<a href="#Benchmarking-Results-Summary-for-Baseline-GET-Request">click here for results</a>
</p>

```bash
ab -n 1000 -c 100 http://127.0.0.1:5000/items
```
*Sends 1,000 GET requests with 100 concurrent connections.*

### Additional Apache Bench Tests- 

- **Time-Bound Test:**<p>
<a href="#Benchmarking-Results-Summary-for-Time-Bound-GET-Request">click here for results</a>
</p>

  ```bash
  ab -t 30 -c 50 http://127.0.0.1:5000/items
  ```
  *Runs the test for 30 seconds with 50 concurrent requests.*

---

- **KeepAlive Test:**<p>
<a href="#Benchmarking-Results-Summary-for-Keep-Alive-GET-Request">click here for results</a>
</p>

  ```bash
  ab -n 1000 -c 100 -k http://127.0.0.1:5000/items
  ```
  *Enables HTTP KeepAlive to reuse connections across multiple requests.*

---

- **Custom Header Test:**<p>
<a href="#Benchmarking-Results-Summary-for-Customer-Header-GET-Request">click here for results</a>
</p>

  ```bash
  ab -n 500 -c 50 -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/items
  ```
  *Includes a custom header (e.g., for authentication) in each request.*

---

- **POST Request Test:**<p>
<a href="#Benchmarking-Results-Summary-for-Post-Request">click here for results</a>
</p>

  1. Create a `postdata.json` file with your JSON payload.
  2. Run:
```bash
ab -n 500 -c 50 -p postdata.json -T "application/json" http://127.0.0.1:5000/items
```
  *Simulates POST requests with the provided JSON data.*

---

- **High Concurrency Stress Test:**<p>
<a href="#Benchmarking-Results-Summary-for-High-Concurrency-GET-Request">click here for results</a>
</p>

```bash
ab -n 10000 -c 500 http://127.0.0.1:5000/items
```
  *Pushes the server to its limits by increasing both the total number of requests and the concurrency level.*

---

## Python Load Testing Scripts

In addition to Apache Bench, this project includes custom Python scripts that perform load tests on your API using the `requests` library. These scripts demonstrate two different approaches: sequential (synchronous) requests and concurrent requests using a thread pool.

---

### 1. Synchronous Load Test

This script sends GET requests one after another until 200 requests have been completed. It prints the HTTP status code for each request and keeps a running tally of the total number of requests and the cumulative count of rows returned from the API (assuming the response is a JSON list).

#### How It Works
- **Sequential Requests:** The script loops, sending a request and then processing the response.
- **Counting:** It increments a counter for each request and aggregates the length of the JSON response.
- **Termination:** The loop stops after 200 requests.

#### Code
```python
import requests
import threading
import time

# Replace with your server's public IP or domain (e.g., http://yourdomain.com)
BASE_URL = 'http://127.0.0.1:5000'

def send_get_requests():
    counter = 0
    row_counter = 0
    while True:
        result = requests.get(BASE_URL + "/items")
        counter += 1
        row_counter += len(result.json())
        print(result.status_code)
        print(counter, row_counter)
        if counter == 200:
            break
        # Uncomment the next line to add a delay between requests
        # time.sleep(1)
        
send_get_requests()
```

---

### 2. Concurrent Load Test

This script uses Python’s `concurrent.futures.ThreadPoolExecutor` to send multiple GET requests concurrently. It simulates a scenario where multiple clients access your API at the same time.

#### How It Works
- **Concurrency:** A thread pool executor manages multiple worker threads.
- **Task Submission:** 500 GET requests are submitted to the thread pool.
- **Results:** As each request completes, its status code and the length of the JSON response are printed.
- **Realistic Load:** This approach better simulates simultaneous user access to your API.

#### Code
```python
import requests
import concurrent.futures

BASE_URL = 'http://127.0.0.1:5000'

def get_items():
    response = requests.get(BASE_URL + "/items")
    return response.status_code, len(response.json())

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_items) for _ in range(500)]
    for future in concurrent.futures.as_completed(futures):
        status, row_count = future.result()
        print(status, row_count)
```

---

## How to Run the Tests

1. **Apache Bench Tests:**
   - Ensure Apache Bench is installed and available in your PATH.
   - Open your terminal (or Git Bash) and run the commands provided in the Apache Bench section.

2. **Python Load Testing Scripts:**
   - Customize the Python scripts if needed.
   - Run the synchronous test with:
     ```bash
     python synchronous_load_test.py
     ```
   - Run the concurrent test with:
     ```bash
     python concurrent_load_test.py
     ```

---

## Consolidated Results Summary

### Overview of Benchmarking Results

The tests cover multiple scenarios including baseline, time-bound, keep-alive, custom header, POST, and high concurrency GET requests. Key takeaways include:

- **Baseline GET Request:**  
  - **Throughput:** ~288 requests/sec  
  - **Latency:** Mean of 347 ms  
  - **Connections:** 100 concurrent connections with stable response times.

- **Time-Bound GET Request:**  
  - **Throughput:** ~311 requests/sec  
  - **Latency:** Mean of 161 ms with a narrow percentile range, indicating consistent performance under a 30-second window.

- **Keep-Alive GET Request:**  
  - **Throughput:** ~289 requests/sec  
  - **Latency:** Mean of 346 ms with efficient connection reuse via persistent connections.

- **Custom Header GET Request:**  
  - **Throughput:** ~320 requests/sec  
  - **Latency:** Mean of 156 ms, demonstrating minimal overhead despite the added header.

- **POST Request Test:**  
  - **Throughput:** ~1283 requests/sec  
  - **Latency:** Mean of 39 ms, though all responses returned were non-2xx, suggesting possible intentional error handling or validation behavior.

- **High Concurrency GET Request:**  
  - **Throughput:** ~288 requests/sec under extreme load (500 concurrent connections)  
  - **Latency:** Mean of 1736 ms, with the 50th percentile at 1617 ms, highlighting increased response times under heavy load.

Overall, the results provide a comprehensive view of system performance across different load scenarios, helping identify both strengths (stable throughput under moderate load) and potential areas for improvement (latency increases under very high concurrency).

---

## Graphical Analysis of Performance Tests

We generated three key graphs to visualize and understand our load test results:

1. **Predicted Mean Latency for Larger Request Quantities**  
![Predicted Mean Latency Graph](graphs\latency_prediction.png)


   - **What It Shows:**  
     - A simple linear extrapolation from our measured data points suggests that as total requests grow, average latency could increase significantly.  
     - Real-world performance may deviate from a neat linear pattern once new bottlenecks (e.g., CPU, memory, database) emerge.  
   - **Why It Matters:**  
     - Offers a rough forecast for capacity planning.  
     - Encourages gathering more data points and testing under varied conditions, rather than relying solely on linear predictions.

1. **Concurrency vs. Requests per Second (RPS) and Latency**  
![Predicted Mean Latency Graph](graphs\concurrency_graph.png)
   - **What It Shows:**  
     - As concurrency increases (i.e., more simultaneous users), the server’s throughput (RPS) initially rises but may plateau or drop once resource limits are reached.  
     - Latency often increases more steadily, indicating that individual requests slow down under heavier concurrent load.  
   - **Why It Matters:**  
     - Reveals the concurrency “sweet spot” before resource contention causes latency to spike.  
     - Helps identify bottlenecks (e.g., thread pools, database connections) when concurrency is too high.

2. **Performance Metrics vs. Total Requests**  
![Predicted Mean Latency Graph](graphs\total_requests_graph.png)
   - **What It Shows:**  
     - When total requests are incremented while concurrency remains constant, throughput (RPS) and mean latency can show different trends.  
     - RPS might peak or remain stable at moderate request volumes, while latency may vary based on how resources are consumed over time.  
   - **Why It Matters:**  
     - Shows how the system handles sustained or long-running load scenarios.  
     - Highlights the point at which the system might start slowing down or saturating due to higher total requests.

### Linking to Kubernetes

These graphs demonstrate how application performance can vary based on concurrency, total requests, and potential resource bottlenecks. As load grows, higher latency and reduced throughput can occur if the system isn’t scaled appropriately. This is where Kubernetes shines:

- **Dynamic Scaling:** Kubernetes can automatically spin up additional pods (instances) when concurrency or total requests surge.  
- **Efficient Resource Management:** By distributing traffic, Kubernetes helps keep latency lower and throughput higher under varying loads.

Below, in [Why We Need Kubernetes](#why-we-need-kubernetes), we’ll explore how Kubernetes can address these performance challenges.


---

## Why We Need Kubernetes

As our load testing results indicate, system performance can vary significantly with the number of concurrent requests. While our compute service shows strong throughput and stable performance under moderate loads, extreme scenarios (like the high concurrency test) reveal increased latencies and potential bottlenecks.

### Key Reasons to Adopt Kubernetes

- **Scalability:**  
  Kubernetes enables automatic scaling of applications based on load. If your service experiences spikes in traffic (as simulated by our high concurrency test), Kubernetes can spin up additional pods to handle the load, maintaining performance and reducing latency.

- **Resilience and High Availability:**  
  With features like self-healing and automated rollouts, Kubernetes ensures that your applications remain available even under heavy stress. This is essential when real-world usage mirrors load testing scenarios where hundreds of requests are handled concurrently.

- **Resource Optimization:**  
  Kubernetes allows for better utilization of system resources through efficient load balancing and resource allocation. Our testing shows that while throughput remains consistent, latency can suffer under high load—Kubernetes can help mitigate this by dynamically distributing the workload.

- **Consistency Across Environments:**  
  As our tests have demonstrated variable performance under different configurations (GET, POST, Keep-Alive, etc.), Kubernetes provides a consistent deployment platform that can help manage these variations, ensuring that performance remains robust across development, testing, and production environments.

By leveraging Kubernetes, you can scale your applications effectively to meet increased demand, ensuring that the high throughput observed in our tests is maintained while mitigating latency and resource bottlenecks. This ultimately leads to a more resilient and responsive service that can adapt to changing loads in real time.

---

## Benchmarking Results Sections

<div id="Benchmarking-Results-Summary-for-Baseline-GET-Request">

# Benchmarking Results Summary for Baseline GET Request

Below are the most relevant metrics for compute performance, including throughput, latency, and connection statistics.

---

## Test Summary & Performance Metrics

| **Metric**                    | **Value**                  | **Notes**                                 |
|-------------------------------|----------------------------|-------------------------------------------|
| **Time Taken for Tests**      | 3.474 seconds              | Total duration of the test                |
| **Complete Requests**         | 1000                       | Total number of requests completed        |
| **Failed Requests**           | 0                          | No failures occurred                      |
| **Total Transferred**         | 16,353,000 bytes           | Total data transferred                    |
| **HTML Transferred**          | 16,185,000 bytes           | Size of the document                      |
| **Requests per Second**       | 287.83 #/sec               | Throughput (higher is better)             |
| **Mean Time per Request**     | 347.424 ms                 | Average latency per request               |
| **Transfer Rate**             | 4596.61 Kbytes/sec         | Network throughput                        |
| **Concurrency Level**         | 100                        | Number of simultaneous connections        |

---

## Connection Times (ms)

| **Metric**    | **Min** | **Mean** | **Std Dev** | **Median** | **Max** |
|---------------|---------|----------|-------------|------------|---------|
| **Connect**   | 0       | 0        | 0.3         | 0          | 2       |
| **Processing**| 20      | 339      | 61.7        | 347        | 504     |
| **Waiting**   | 3       | 321      | 62.0        | 330        | 490     |
| **Total**     | 20      | 339      | 61.7        | 347        | 504     |

---

## Request Percentiles (ms)

| **Percentile** | **Response Time (ms)** |
|----------------|------------------------|
| 50%            | 347                    |
| 66%            | 362                    |
| 75%            | 370                    |
| 80%            | 377                    |
| 90%            | 394                    |
| 95%            | 412                    |
| 98%            | 434                    |
| 99%            | 451                    |
| 100% (Max)     | 504                    |

---

### Key Points for Compute

- **Throughput:** The server handled ~288 requests per second.
- **Latency:** The average time per request is 347 ms, with most requests served within 347–394 ms.
- **Consistency:** Zero failed requests indicate stable compute performance.
- **Connection Times:** Processing times (average ~339 ms) and percentiles help understand the tail latency, which is critical for high-load compute scenarios.

These metrics help you gauge not only the raw performance (throughput and latency) but also the quality of response times across different percentiles, which is especially important for compute-intensive applications.
</div>

---

<div id="Benchmarking-Results-Summary-for-Time-Bound-GET-Request">

# Benchmarking Results Summary for Time-Bound Get Requests

Below are the most relevant metrics for compute performance, including throughput, latency, and connection statistics.

---

## Test Summary & Performance Metrics

| **Metric**                    | **Value**                  | **Notes**                                            |
|-------------------------------|----------------------------|------------------------------------------------------|
| **Time Taken for Tests**      | 30.013 seconds             | Total duration of the test                           |
| **Complete Requests**         | 9343                       | Total number of requests completed                   |
| **Failed Requests**           | 0                          | No failures occurred                                 |
| **Total Transferred**         | 152,802,432 bytes          | Total data transferred                               |
| **HTML Transferred**          | 151,232,640 bytes          | Size of the document (payload)                       |
| **Requests per Second**       | 311.29 #/sec               | Throughput (higher is better)                        |
| **Mean Time per Request**     | 160.619 ms                 | Average latency per request (sequential handling)    |
| **Transfer Rate**             | 4971.83 Kbytes/sec         | Network throughput                                   |
| **Concurrency Level**         | 50                         | Number of simultaneous connections                   |

---

## Connection Times (ms)

| **Metric**     | **Min** | **Mean** | **Std Dev** | **Median** | **Max** |
|----------------|---------|----------|-------------|------------|---------|
| **Connect**    | 0       | 0        | 0.3         | 0          | 2       |
| **Processing** | 20      | 160      | 19.2        | 161        | 237     |
| **Waiting**    | 3       | 143      | 18.7        | 144        | 224     |
| **Total**      | 20      | 160      | 19.2        | 161        | 237     |

---

## Request Percentiles (ms)

| **Percentile**   | **Response Time (ms)** |
|------------------|------------------------|
| 50%              | 161                    |
| 66%              | 167                    |
| 75%              | 170                    |
| 80%              | 173                    |
| 90%              | 180                    |
| 95%              | 188                    |
| 98%              | 196                    |
| 99%              | 201                    |
| 100% (Max)       | 237                    |

---

### Key Points for Compute

- **Throughput:** The server handled approximately 311 requests per second.
- **Latency:** The mean time per request is around 161 ms, with most requests falling between 161–180 ms.
- **Consistency:** With zero failed requests, the test indicates stable compute performance under a load of 50 concurrent connections.
- **Connection Times:** The connection phase is nearly instantaneous, while the processing (and waiting) phases provide insight into the server’s response time distribution.
- **Percentile Analysis:** The request percentiles show that even the slowest requests (up to 237 ms) remain within a tight range, which is valuable for assessing performance under load.
- 
</div>
---

<div id="Benchmarking-Results-Summary-for-Keep-Alive-GET-Request">

# Benchmarking Results Summary for Keep-Alive GET Requests

Below are the results of a keep-alive GET requests benchmark, showing progress updates, server details, performance metrics, connection times, and percentile distribution.

---

## Test Progress

- Completed 100 requests  
- Completed 200 requests  
- Completed 300 requests  
- Completed 400 requests  
- Completed 500 requests  
- Completed 600 requests  
- Completed 700 requests  
- Completed 800 requests  
- Completed 900 requests  
- Completed 1000 requests  
- Finished 1000 requests  

---

## Server Information

- **Server Software:** Werkzeug/3.1.3  
- **Server Hostname:** 127.0.0.1  
- **Server Port:** 5000  
- **Document Path:** /items  
- **Document Length:** 16185 bytes  

---

## Test Summary & Performance Metrics

| **Metric**                      | **Value**                | **Notes**                                          |
|---------------------------------|--------------------------|----------------------------------------------------|
| **Concurrency Level**           | 100                      | Number of simultaneous connections               |
| **Time taken for tests**        | 3.464 seconds            | Total duration of the test                         |
| **Complete Requests**           | 1000                     | Total number of requests completed                 |
| **Failed Requests**             | 0                        | No failures occurred                               |
| **Keep-Alive Requests**         | 0                        | Number of keep-alive requests (if applicable)      |
| **Total Transferred**           | 16,353,000 bytes         | Total data transferred                             |
| **HTML Transferred**            | 16,185,000 bytes         | Size of the document (payload)                     |
| **Requests per Second**         | 288.68 #/sec             | Throughput (higher is better)                      |
| **Mean Time per Request**       | 346.402 ms               | Average latency per request                        |
| **Time per Request (Concurrent)** | 3.464 ms             | Average time per request across concurrent connections |
| **Transfer Rate**               | 4610.18 Kbytes/sec       | Network throughput                                 |

---

## Connection Times (ms)

| **Metric**     | **Min** | **Mean** | **Std Dev** | **Median** | **Max** |
|----------------|---------|----------|-------------|------------|---------|
| **Connect**    | 0       | 0        | 0.3         | 0          | 2       |
| **Processing** | 15      | 338      | 51.1        | 346        | 484     |
| **Waiting**    | 1       | 322      | 50.9        | 330        | 470     |
| **Total**      | 16      | 339      | 51.1        | 346        | 484     |

---

## Request Percentiles (ms)

| **Percentile**   | **Response Time (ms)** |
|------------------|------------------------|
| 50%              | 346                    |
| 66%              | 359                    |
| 75%              | 367                    |
| 80%              | 374                    |
| 90%              | 392                    |
| 95%              | 405                    |
| 98%              | 423                    |
| 99%              | 442                    |
| 100% (Max)       | 484                    |

---

### Key Points for Keep-Alive Testing

- **Keep-Alive Feature:**  
  This test evaluates performance using HTTP persistent connections. By reusing a single connection for multiple requests, it reduces the overhead of establishing new connections for each request.

- **Throughput:**  
  The server handled approximately 289 requests per second.

- **Latency:**  
  The mean time per request is around 346 ms, reflecting overall response time under load.

- **Connection Efficiency:**  
  Minimal connection times with detailed processing times help you understand the request handling efficiency.

- **Percentile Analysis:**  
  The distribution shows that even the slowest requests (up to 484 ms) remain within an acceptable range, which is important for assessing performance consistency under load.

This comprehensive summary provides insights into your server’s performance with keep-alive GET requests.
</div>

---
<div id="Benchmarking-Results-Summary-for-Customer-Header-GET-Request">

# Benchmarking Results Summary for Custom Header GET Requests

Below are the results of a benchmark test using custom headers on GET requests. The report includes progress updates, server details, performance metrics, connection times, and percentile distributions.

---

## Test Progress

- Completed 100 requests  
- Completed 200 requests  
- Completed 300 requests  
- Completed 400 requests  
- Completed 500 requests  
- Finished 500 requests  

---

## Server Information

- **Server Software:** Werkzeug/3.1.3  
- **Server Hostname:** 127.0.0.1  
- **Server Port:** 5000  
- **Document Path:** /items  
- **Document Length:** 16185 bytes  

---

## Test Summary & Performance Metrics

| **Metric**                      | **Value**                | **Notes**                                          |
|---------------------------------|--------------------------|----------------------------------------------------|
| **Concurrency Level**           | 50                       | Number of simultaneous connections               |
| **Time taken for tests**        | 1.564 seconds            | Total duration of the test                         |
| **Complete Requests**           | 500                      | Total number of requests completed                 |
| **Failed Requests**             | 0                        | No failures occurred                               |
| **Total Transferred**           | 8,176,500 bytes          | Total data transferred                             |
| **HTML Transferred**            | 8,092,500 bytes          | Size of the document (payload)                     |
| **Requests per Second**         | 319.71 #/sec             | Throughput (higher is better)                      |
| **Mean Time per Request**       | 156.391 ms               | Average latency per request                        |
|
<div>

---
<div id="Benchmarking-Results-Summary-for-Post-Request">

# Benchmarking Results Summary for POST Requests

Below are the results from a POST request benchmark test, showing progress updates, server details, performance metrics, connection times, and percentile distributions.

---

## Test Progress

- Completed 100 requests  
- Completed 200 requests  
- Completed 300 requests  
- Completed 400 requests  
- Completed 500 requests  
- Finished 500 requests  

---

## Server Information

- **Server Software:** Werkzeug/3.1.3  
- **Server Hostname:** 127.0.0.1  
- **Server Port:** 5000  
- **Document Path:** /items  
- **Document Length:** 153 bytes  

---

## Test Summary & Performance Metrics

| **Metric**                      | **Value**                | **Notes**                                          |
|---------------------------------|--------------------------|----------------------------------------------------|
| **Concurrency Level**           | 50                       | Number of simultaneous connections               |
| **Time taken for tests**        | 0.390 seconds            | Total duration of the test                         |
| **Complete Requests**           | 500                      | Total number of requests completed                 |
| **Failed Requests**             | 0                        | No failures occurred                               |
| **Non-2xx Responses**           | 500                      | All responses returned were non-2xx (likely POST)  |
| **Total Transferred**           | 185,000 bytes            | Total data transferred                             |
| **Total Body Sent**             | 246,500 bytes            | Total payload sent                                  |
| **HTML Transferred**            | 76,500 bytes             | Size of the document (payload)                     |
| **Requests per Second**         | 1283.19 #/sec            | Throughput (higher is better)                      |
| **Mean Time per Request**       | 38.965 ms                | Average latency per request                        |
| **Time per Request (Concurrent)** | 0.779 ms              | Average time per request across concurrent requests|
| **Transfer Rate**               | 463.65 Kbytes/sec (received) <br> 617.78 kb/s (sent) <br> 1081.44 kb/s total | Network throughput |

---

## Connection Times (ms)

| **Metric**     | **Min** | **Mean** | **Std Dev** | **Median** | **Max** |
|----------------|---------|----------|-------------|------------|---------|
| **Connect**    | 0       | 0        | 0.3         | 0          | 2       |
| **Processing** | 13      | 36       | 6.5         | 35         | 61      |
| **Waiting**    | 2       | 18       | 5.6         | 18         | 35      |
| **Total**      | 13      | 37       | 6.5         | 35         | 61      |

---

## Request Percentiles (ms)

| **Percentile**   | **Response Time (ms)** |
|------------------|------------------------|
| 50%              | 35                     |
| 66%              | 38                     |
| 75%              | 41                     |
| 80%              | 42                     |
| 90%              | 46                     |
| 95%              | 47                     |
| 98%              | 48                     |
| 99%              | 55                     |
| 100% (Max)       | 61                     |

---

### Key Points for POST Request Testing

- **POST vs GET Behavior:**  
  In this test, although the results mention "POST Request GET Requests," it appears that you're benchmarking how the server handles POST requests (possibly with a specific data payload). Note that all responses were non-2xx, which might indicate the server is returning a status code that isn't in the 200 range (this could be intentional if testing error handling or expected behavior).

- **Throughput:**  
  The server processed approximately 1283 requests per second, demonstrating high throughput under the test conditions.

- **Latency:**  
  The mean time per request was about 39 ms, with most requests completing in under 61 ms. This suggests a very responsive endpoint even under load.

- **Connection Efficiency:**  
  The low connection times indicate that the overhead for establishing connections is minimal, with most of the time spent in processing and waiting phases.

- **Payload Consideration:**  
  The total body sent (246,500 bytes) versus HTML transferred (76,500 bytes) indicates the request payload size compared to the server’s response.

This detailed summary provides insights into your server’s performance when handling POST requests under load, helping you assess throughput, latency, and overall response efficiency.

<div>
---

<div id="Benchmarking-Results-Summary-for-High-Concurrency-GET-Request">

# Benchmarking Results Summary for High-Concurrency GET Requests

Below are the results from a high-concurrency GET requests benchmark test, showing progress updates, server details, performance metrics, connection times, and percentile distributions.

---

## Test Progress

- Completed 1000 requests  
- Completed 2000 requests  
- Completed 3000 requests  
- Completed 4000 requests  
- Completed 5000 requests  
- Completed 6000 requests  
- Completed 7000 requests  
- Completed 8000 requests  
- Completed 9000 requests  
- Completed 10000 requests  
- Finished 10000 requests  

---

## Server Information

- **Server Software:** Werkzeug/3.1.3  
- **Server Hostname:** 127.0.0.1  
- **Server Port:** 5000  
- **Document Path:** /items  
- **Document Length:** 16185 bytes  

---

## Test Summary & Performance Metrics

| **Metric**                      | **Value**                     | **Notes**                                         |
|---------------------------------|-------------------------------|---------------------------------------------------|
| **Concurrency Level**           | 500                           | Number of simultaneous connections                |
| **Time taken for tests**        | 34.717 seconds                | Total duration of the test                         |
| **Complete Requests**           | 10000                         | Total number of requests completed                 |
| **Failed Requests**             | 0                             | No failures occurred                               |
| **Total Transferred**           | 163,530,000 bytes             | Total data transferred                             |
| **HTML Transferred**            | 161,850,000 bytes             | Size of the document (payload)                     |
| **Requests per Second**         | 288.04 #/sec                  | Throughput (mean)                                  |
| **Mean Time per Request**       | 1735.867 ms                   | Average latency per request                        |
| **Time per Request (Concurrent)** | 3.472 ms                    | Average time per request across concurrent requests|
| **Transfer Rate**               | 4599.93 Kbytes/sec received   | Network throughput                                 |

---

## Connection Times (ms)

| **Metric**     | **Min** | **Mean** | **Std Dev** | **Median** | **Max** |
|----------------|---------|----------|-------------|------------|---------|
| **Connect**    | 0       | 3        | 40.5        | 0          | 517     |
| **Processing** | 169     | 1686     | 302.3       | 1617       | 2146    |
| **Waiting**    | 3       | 1068     | 451.8       | 1063       | 2132    |
| **Total**      | 169     | 1689     | 303.7       | 1617       | 2146    |

---

## Request Percentiles (ms)

| **Percentile**   | **Response Time (ms)** |
|------------------|------------------------|
| 50%              | 1617                   |
| 66%              | 1625                   |
| 75%              | 1629                   |
| 80%              | 2108                   |
| 90%              | 2122                   |
| 95%              | 2129                   |
| 98%              | 2133                   |
| 99%              | 2137                   |
| 100% (Max)       | 2146                   |

---

### Key Points for High-Concurrency Testing

- **Throughput:**  
  The server processed approximately 288 requests per second under a load of 500 concurrent connections.

- **Latency:**  
  The mean time per request is around 1736 ms, with 50% of the requests served in 1617 ms. This indicates a high load scenario where individual request times are significantly increased.

- **Connection Times:**  
  The breakdown shows that processing and waiting times dominate the total request time, which is expected when handling 500 concurrent connections.

- **Percentile Analysis:**  
  The majority of requests fall between 1617 ms and 2146 ms, indicating that while most responses are consistent, there is some variability under high load.

This detailed summary provides insight into the server’s performance under high concurrency, useful for understanding its scalability and responsiveness when managing a large number of simultaneous requests.
<div>

---

## Contributing

Contributions and feedback are welcome! Feel free to open an issue or submit a pull request with improvements or new tests.

---

Happy Load Testing!
