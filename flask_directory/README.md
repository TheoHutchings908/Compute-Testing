
# Python Flask & SQLite App

A minimal Flask application that serves data from an SQLite database. Includes a Dockerfile for easy containerization.

---

<details>
<summary>Example Directory Tree</summary>

**Project Structure**

```plaintext
.
├── .venv/               # (Optional) Virtual environment (ignored via .gitignore)
├── python_host/         # (Optional) Directory for additional Python files
├── database.db          # SQLite database file
├── Dockerfile           # Docker container configuration
├── python_flask.py      # Main Flask application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

</details>

---

### 1. Local Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/YourUser/YourRepo.git
   cd YourRepo
   ```
2. **(Optional) Create a Virtual Environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the App**  
   ```bash
   python python_flask.py
   ```
   - The app runs on **port 5000** by default.
   - Visit ["your_local_host_ip"/items]("your_local_host_ip"/items) to see the JSON data.

---

### 2. Docker Setup
#### *Please note, if you are running this on a server, you will need to replace localhost ip with your server ip*

1. **Build the Docker Image**  
   ```bash
   docker build -t flask-sqlite-app .
   ```

2. **Run the Container**  
   ```bash
   docker run -d -p 5000:5000 --name flask-sqlite-container flask-sqlite-app
   ```
   - Access ["your_local_host_ip"/items]("your_local_host_ip"/items) to confirm the app is running.

3. **Stop & Remove the Container (Optional)**  
   ```bash
   docker stop flask-sqlite-container
   docker rm flask-sqlite-container
   ```

---

### Flask Endpoints

- **GET /items**  
  Returns all rows from the `customers` table in JSON format.  
  Example response:
  ```json
  [
    {
      "CustomerId": 1,
      "FirstName": "Luís",
      "LastName": "Gonçalves",
      ...
    },
    ...
  ]
  ```

*Note: A POST endpoint is included as commented code in `python_flask.py` if you wish to enable adding new items.*

---

### SQLite Database

- **database.db** contains the `customers` table (and possibly other tables).  
- Modify or inspect the data using `sqlite3` or any SQLite client:
  ```bash
  sqlite3 database.db
  ```

---

### Tips & Notes

- Keep your virtual environment directory (e.g., `.venv/`) in your `.gitignore`.
- Update `requirements.txt` using:
  ```bash
  pip freeze > requirements.txt
  ```
- For production deployments, consider pushing your Docker image to a container registry.

---

### Contributing

1. **Fork the Repository** and create your feature branch.
2. **Commit Changes** with clear messages.
3. **Push** your changes to your fork.
4. **Submit a Pull Request** for review.


---

Happy Coding!
```

