import requests

url = "http://127.0.0.1:8000/start_task"
data = {
    "duration": 10,
    "callback_url": "http://example.com/callback"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
