from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()

    if data is None:
        return "No JSON received", 400

    log_entry = f"{datetime.now()} | {data}\n"

    try:
        with open("log.txt", "a") as f:
            f.write(log_entry)
        print("✅ Data saved to log.txt")
    except Exception as e:
        print("❌ Failed to write log:", e)

    print("Received:", data)
    return 'Data received and saved', 200

