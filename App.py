from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {}
chats = []

@app.route('/')
def home():
    return "Welcome to Z-chat - By Zobi Official"

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({"status": "failed", "message": "ID pehle se bani hui hai"})
    users[username] = password
    return jsonify({"status": "success", "message": f"{username} Z-chat par ban gaya"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if users.get(username) == password:
        token = f"zchat_token_{username}_12345"
        return jsonify({"status": "success", "token": token, "user": username})
    else:
        return jsonify({"status": "failed", "message": "Password ghalat hai"})

@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    chats.append(data)
    return jsonify({"status": "success"})

@app.route('/api/chats', methods=['GET'])
def get_chats():
    return jsonify(chats)
