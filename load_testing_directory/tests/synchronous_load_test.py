import requests
import threading
import time

# Replace with your server's public IP or domain (e.g., http://yourdomain.com)
BASE_URL = 'your_localhost_ip'


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
        #time.sleep(1)
        
send_get_requests()
        
        