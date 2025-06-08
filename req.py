import requests

url = "https://your-render-url.onrender.com/receive"  # Replace with your actual Render URL

data = {
    "browser_password": "test_1234",
    "username": "rojan"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
