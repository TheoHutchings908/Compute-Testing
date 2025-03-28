import requests
import concurrent.futures

BASE_URL = 'your_localhost_ip'


def get_items():
    response = requests.get(BASE_URL + "/items")
    return response.status_code, len(response.json())

    
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_items) for _ in range(500)]
    for future in concurrent.futures.as_completed(futures):
        status, row_count = future.result()
        print(status, row_count)