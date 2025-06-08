from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()

    if data is None:
        return "No JSON received", 400

    log_entry = f"{datetime.now()} | {data}\n"

    # Save the data to a file
    with open("log.txt", "a") as f:
        f.write(log_entry)

    print("Received:", data)
    return 'Data received and saved', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
