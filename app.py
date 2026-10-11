from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

users = {}
logs = []
messages = []

ADMIN_HTML = """
<html><head><style>
body{font-family:sans-serif;padding:20px;background:#f5f5f5}
table{width:100%;border-collapse:collapse;background:white}
th,td{border:1px solid #ccc;padding:8px;text-align:left}
h1{color:#6a11cb}
</style></head><body>
<h1>Z-chat Admin Panel - By Zobi Official</h1>
<h3>Total Users: {{total_users}} | Total Messages: {{total_msgs}}</h3>
<hr><h2>Logs (Signup/Login)</h2>
<table><tr><th>Time</th><th>User</th><th>Action</th></tr>
{% for l in logs %}<tr><td>{{l.time}}</td><td>{{l.user}}</td><td>{{l.action}}</td></tr>{% endfor %}
</table><hr><h2>All Users</h2><ul>{% for u in users %}<li>{{u}}</li>{% endfor %}</ul>
<hr><h2>Recent Chats</h2><ul>{% for m in messages[-20:] %}<li><b>{{m['from']}} -> {{m['to']}}:</b> {{m['text']}} <i>{{m['time']}}</i></li>{% endfor %}</ul>
</body></html>
"""

@app.route('/')
def home():
    return "Z-chat API is Live - By Zobi"

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_HTML, users=users, logs=logs, messages=messages, total_users=len(users), total_msgs=len(messages))

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    u=data.get('username'); p=data.get('password')
    if not u or not p: return jsonify({"status":"failed","message":"ID Password do"})
    if u in users: return jsonify({"status":"failed","message":"ID pehle se hai"})
    users[u]=p
    logs.append({"user":u,"action":"Signup","time":str(datetime.now())})
    return jsonify({"status":"success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u=data.get('username'); p=data.get('password')
    if users.get(u)==p:
        logs.append({"user":u,"action":"Login","time":str(datetime.now())})
        return jsonify({"status":"success","user":u})
    return jsonify({"status":"failed","message":"Ghalat password"})

@app.route('/api/search', methods=['GET'])
def search():
    q=request.args.get('q','').lower()
    result=[u for u in users if q in u.lower()]
    return jsonify(result)

@app.route('/api/send', methods=['POST'])
def send():
    data=request.json
    data['time']=str(datetime.now())
    messages.append(data)
    return jsonify({"status":"success"})

@app.route('/api/chats', methods=['GET'])
def get_chats():
    user1=request.args.get('user1')
    user2=request.args.get('user2')
    filtered=[m for m in messages if (m['from']==user1 and m['to']==user2) or (m['from']==user2 and m['to']==user1)]
    return jsonify(filtered)

@app.route('/api/users', methods=['GET'])
def all_users():
    return jsonify(list(users.keys()))
