from flask import Flask, request

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()
    print("Received:", data)
    return 'Received OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
