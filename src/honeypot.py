import socket, threading, sqlite3, json, datetime, paramiko, os

with open('config.json', 'r', encoding='utf-8-sig') as f:
    CONFIG = json.load(f)

def setup_db():
    db_path = CONFIG['database']['name']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attacks (id INTEGER PRIMARY KEY, timestamp TEXT, ip TEXT, username TEXT, password TEXT, method TEXT)''')
    conn.commit()
    return conn

def sanitize_input(data):
    if not data: return ""
    return str(data).replace('\n', '').replace('\r', '').strip()[:50]

class SecureSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip, db_conn):
        self.client_ip = client_ip
        self.db_conn = db_conn

    def check_auth_password(self, username, password):
        self.log_attack(username, password, "Password Auth")
        return paramiko.AUTH_FAILED 

    def log_attack(self, user, pwd, method):
        safe_user = sanitize_input(user)
        safe_pwd = sanitize_input(pwd)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[!] ALERT [{method}] from {self.client_ip} -> User: {safe_user} | Pass: {safe_pwd}")
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO attacks (timestamp, ip, username, password, method) VALUES (?, ?, ?, ?, ?)", (timestamp, self.client_ip, safe_user, safe_pwd, method))
        self.db_conn.commit()

def handle_connection(client, addr, db_conn):
    transport = paramiko.Transport(client)
    transport.local_version = CONFIG['honeypot']['banner']
    transport.add_server_key(paramiko.RSAKey.generate(2048))
    server = SecureSSHServer(addr[0], db_conn)
    try:
        transport.start_server(server=server)
        while transport.is_active(): threading.Event().wait(1)
    except Exception: pass
    finally: transport.close()

def start_honeypot():
    db_conn = setup_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((CONFIG['honeypot']['bind_ip'], CONFIG['honeypot']['port']))
    server_socket.listen(100)
    print(f"[*] SentinelTrap v2 Online. Hostname: {CONFIG['honeypot']['hostname']}")
    print(f"[*] Listening on port {CONFIG['honeypot']['port']}...")
    while True:
        try:
            client, addr = server_socket.accept()
            threading.Thread(target=handle_connection, args=(client, addr, db_conn), daemon=True).start()
        except KeyboardInterrupt: break

if __name__ == "__main__": start_honeypot()
