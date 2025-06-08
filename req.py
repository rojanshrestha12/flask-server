import requests

url = "http://localhost:5000/upload"
files = {'file': open('password.txt', 'rb')}

res = requests.post(url, files=files)
print("Status:", res.status_code)
print("Response:", res.text)
