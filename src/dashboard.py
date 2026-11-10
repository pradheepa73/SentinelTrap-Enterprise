import sqlite3, pandas as pd, json, os
from jinja2 import Template

with open('config.json', 'r', encoding='utf-8-sig') as f: CONFIG = json.load(f)

def generate_dashboard():
    db_path = CONFIG['database']['name']
    if not os.path.exists(db_path): return print("[!] No DB found.")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM attacks", conn)
    if df.empty: return print("[*] No attacks logged yet.")
    
    html = """<html><head><title>SentinelTrap</title><style>body{font-family:Arial;background:#0d1117;color:white;padding:20px;} .card{background:#161b22;padding:20px;margin-bottom:20px;} h1{color:#58a6ff;} table{width:100%;border-collapse:collapse;} th,td{padding:10px;border-bottom:1px solid #30363d;}</style></head>
    <body><h1>🛡️ SentinelTrap Analytics</h1><div class="card"><h3>Total Attacks: {{ total }}</h3><h3>Unique IPs: {{ ips }}</h3></div>
    <table><tr><th>Time</th><th>IP</th><th>User</th><th>Pass</th></tr>
    {% for row in data %}<tr><td>{{ row['timestamp'] }}</td><td style="color:#58a6ff;">{{ row['ip'] }}</td><td>{{ row['username'] }}</td><td style="color:#3fb950;">{{ row['password'] }}</td></tr>{% endfor %}</table></body></html>"""
    
    output = Template(html).render(total=len(df), ips=df['ip'].nunique(), data=df.to_dict('records'))
    os.makedirs('evidence', exist_ok=True)
    with open("evidence/dashboard.html", "w", encoding="utf-8-sig") as f: f.write(output)
    print("[+] Dashboard generated: evidence/dashboard.html")

if __name__ == "__main__": generate_dashboard()
