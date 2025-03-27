# Python Flask & SQLite App - Project Summary

This project is a minimal Flask application that serves data from an SQLite database. It demonstrates how to build a simple RESTful API with a lightweight Python backend and provides a Dockerfile for containerized deployments and then tests the load capacity when sending multiple GET and POST requests.

## Key Features

- **REST API Endpoint:**  
  - The `/items` endpoint returns customer data stored in an SQLite database in JSON format.

- **Docker Containerization:**  
  - The included Dockerfile makes it easy to build and run the application in a container, ensuring a consistent environment across different systems.

- **Local Setup & Deployment:**  
  - Detailed instructions are provided for setting up the project locally using a virtual environment, installing dependencies, and running the app.
  - Docker deployment instructions allow for quick containerization and scaling.

- **Load Testing Documentation:**  
  - The repository includes detailed documentation and scripts for load testing the API using Apache Bench (ab) and custom Python scripts, enabling performance analysis and scalability testing.

## Why This Project?

This project serves as a template for building simple, scalable web applications with Python. It is ideal for learning:
- How to create RESTful services with Flask.
- How to work with SQLite for lightweight data storage.
- How to containerize an application using Docker.
- How to perform load testing to understand performance under different conditions.

Whether you’re developing a small project or preparing for a larger scale deployment (with Kubernetes, for example), this project provides a solid foundation.

---

Happy Coding!
