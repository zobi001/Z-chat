from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database
users = {} # {username: password}
logs = [] # signup/login logs
messages = [] # all chats

# Admin Panel HTML
ADMIN_HTML = """
<h1>Z-chat Admin Panel - By Zobi</h1>
<h3>Total Users: {{total_users}}</h3>
<h3>Total Messages: {{total_msgs}}</h3>
<hr>
<h2>Signup / Login Logs</h2>
<table border=1><tr><th>Time</th><th>User</th><th>Action</th></tr>
{% for l in logs %}<tr><td>{{l.time}}</td><td>{{l.user}}</td><td>{{l.action}}</td></tr>{% endfor %}
</table>
<hr>
<h2>All Users</h2>
<ul>{% for u in users %}<li>{{u}}</li>{% endfor %}</ul>
"""

@app.route('/')
def home():
    return "Z-chat API is Live"

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_HTML, users=users, logs=logs, total_users=len(users), total_msgs=len(messages))

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    u = data.get('username'); p = data.get('password')
    if u in users:
        return jsonify({"status":"failed"})
    users[u]=p
    logs.append({"user":u, "action":"Signup", "time": str(datetime.now())})
    return jsonify({"status":"success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u = data.get('username'); p = data.get('password')
    if users.get(u) == p:
        logs.append({"user":u, "action":"Login", "time": str(datetime.now())})
        return jsonify({"status":"success", "user":u})
    return jsonify({"status":"failed"})

@app.route('/api/search', methods=['GET'])
def search():
    q = request.args.get('q','').lower()
    result = [u for u in users if q in u.lower()]
    return jsonify(result)

@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    data['time'] = str(datetime.now())
    messages.append(data)
    return jsonify({"status":"success"})

@app.route('/api/chats', methods=['GET'])
def get_chats():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    # private chat between 2 users
    filtered = [m for m in messages if (m['from']==user1 and m['to']==user2) or (m['from']==user2 and m['to']==user1)]
    return jsonify(filtered)

@app.route('/api/users', methods=['GET'])
def all_users():
    return jsonify(list(users.keys()))
