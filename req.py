import requests

url = "https://your-render-url.onrender.com/upload"

with open("password.txt", "rb") as f:
    files = {'file': ('password.txt', f)}
    res = requests.post(url, files=files)

print("Status:", res.status_code)
print("Response:", res.text)
