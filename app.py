from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import requests, socket, pandas as pd, io, os

app = Flask(__name__)
app.secret_key = 'super_secret_cyber_key' 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id): self.id = id

@login_manager.user_loader
def load_user(user_id): return User(user_id)

def scan_xss(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = soup.find_all('form')
        payload = "<script>alert(1)</script>"
        vulns = []
        for form in forms:
            action = form.attrs.get('action', '').lower()
            target = url if not action else url + action
            inputs = form.find_all('input')
            data = {i.get('name'): payload for i in inputs if i.get('name')}
            r = requests.post(target, data=data, timeout=5)
            if payload in r.text: vulns.append(target)
        return vulns if vulns else ["No XSS found on target."]
    except: return ["Error: Connection timed out or invalid URL."]

def scan_ports(target):
    results = []
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 8080]
    try:
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0: results.append(f"Port {port}: OPEN")
            s.close()
        return results if results else ["No common ports open on target."]
    except: return ["Invalid Target IP"]

def analyze_logs(log_text):
    try:
        data = io.StringIO(log_text)
        df = pd.read_csv(data, sep=" ", header=None, names=["IP", "Date", "Method", "URL", "Status"])
        failed = df[df['Status'] == '401']
        ip_counts = failed['IP'].value_counts()
        alerts = [f"[!] Brute Force Alert: {ip} ({count} fails)" for ip, count in ip_counts.items() if count >= 3]
        return alerts if alerts else ["No attacks found."]
    except: return ["Invalid log format."]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'cyber2026':
            login_user(User('admin'))
            return redirect(url_for('index'))
        return "Invalid Credentials. Try admin / cyber2026"
    return '''
        <body style="background:#0d1117;color:#58a6ff;font-family:monospace;text-align:center;padding-top:100px;">
        <h2>🛡️ SentinelTrap Enterprise Login</h2>
        <form method="POST" style="display:inline-block;background:#161b22;padding:30px;border-radius:8px;border:1px solid #30363d;">
            <input type="text" name="username" placeholder="Username" style="display:block;margin:10px;padding:10px;background:#000;color:#fff;border:1px solid #30363d;"><br>
            <input type="password" name="password" placeholder="Password" style="display:block;margin:10px;padding:10px;background:#000;color:#fff;border:1px solid #30363d;"><br>
            <button type="submit" style="background:#238636;color:#fff;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;">Login</button>
        </form>
        <p>Hint: admin / cyber2026</p>
        </body>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/scan/web', methods=['POST'])
@login_required
def api_web():
    return jsonify({"result": scan_xss(request.json.get('url'))})

@app.route('/api/scan/network', methods=['POST'])
@login_required
def api_net():
    return jsonify({"result": scan_ports(request.json.get('target'))})

@app.route('/api/scan/logs', methods=['POST'])
@login_required
def api_log():
    return jsonify({"result": analyze_logs(request.json.get('logs'))})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
