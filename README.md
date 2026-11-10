
<div align="center">

# SentinelTrap Enterprise
### Unified Cybersecurity Operations & Threat Intelligence Dashboard

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Security](https://img.shields.io/badge/Domain-Cybersecurity-red?style=for-the-badge)](#)

**Submitted To:** Elevate Labs Internship Program  
**Author:** Pradheepa M  

</div>

---

## Executive Summary

In modern Security Operations Centers (SOCs), analysts suffer from "tool fatigue" by pivoting between separate command-line utilities for network scanning, web fuzzing, and log analysis. This fragmentation increases the Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR).

**SentinelTrap Enterprise** solves this by providing a unified, full-stack web dashboard. It consolidates both **Offensive Security** (vulnerability assessment) and **Defensive Security** (deception technology and log triage) into a single, authenticated interface, allowing analysts to operate from a single pane of glass.

---

## Core Modules (Red Team vs. Blue Team)

### Offensive Security (Reconnaissance)
*   **Web Vulnerability Scanner:** Utilizes `BeautifulSoup` and `requests` to crawl target endpoints, identify HTML forms, and inject XSS payloads to test for input sanitization flaws.
*   **Network Port Scanner:** A high-speed TCP socket scanner leveraging Python's native `socket` library to map exposed services (Ports 21, 22, 80, 443, 3306, 3389).

### Defensive Security (Threat Intelligence)
*   **SSH Honeypot (Deception):** Built with `Paramiko`, this live SSH server mimics a vulnerable host to trap brute-force attackers, logging their IP, username, and password into a local SQLite database.
*   **Intrusion Log Analyzer:** A `Pandas`-powered engine that ingests raw web server logs, groups failed authentication attempts, and flags IP addresses exceeding the brute-force threshold (HTTP 401 spikes).

### Platform Security
*   **Role-Based Access Control (RBAC):** The dashboard is protected by session-based authentication. Analysts must authenticate via a secure login portal before executing any offensive scans.

---

## System Architecture

```text
[ Web Browser (Client) ]
       |
       | (HTTPS / REST API)
       v
[ Flask Web Server (app.py) ]
       |
       |---> [ Auth Guard ] ---> Validates Session
       |
       |---> [ Web Scanner ] ---> requests + BeautifulSoup ---> Target URL
       |
       |---> [ Port Scanner ] ---> Python Socket Library ---> Target IP
       |
       |---> [ Log Analyzer ] ---> Pandas DataFrame
       |
       |---> [ Honeypot Viewer ] ---> SQLite3 DB <--- [ Paramiko SSH Server ]
```

---

## Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3, Flask | Routing, API endpoints, session management. |
| **Frontend** | HTML5, CSS3, Vanilla JS | Dark-mode UI, asynchronous Fetch API calls. |
| **Networking** | Socket, Requests | TCP port scanning and HTTP web crawling. |
| **Security** | Paramiko, BeautifulSoup | SSH honeypot emulation and XSS payload injection. |
| **Data & Logs** | Pandas, SQLite3 | Log parsing, anomaly detection, and attack telemetry. |

---

## Local Deployment Guide

Follow these steps to deploy the dashboard on your local machine.

**1. Clone the Repository**
```bash
git clone https://github.com/pradheepa73/SentinelTrap-Enterprise.git
cd SentinelTrap-Enterprise
```

**2. Install Dependencies**
```bash
pip install flask requests beautifulsoup4 pandas paramiko
```

**3. Initialize the Application**
```bash
python app.py
```

**4. Access the Dashboard**
Open your browser and navigate to: `http://127.0.0.1:5000`

| Credential | Value |
| :--- | :--- |
| **Username** | `admin` |
| **Password** | `cyber2026` |

*(Note: To populate the Honeypot Dashboard with live data, execute `python src/honeypot.py` in a separate terminal and simulate an attack).*

---

## Visual Evidence

Here is the live application in action:

**Secure Login Portal**
![Secure Login Portal]<img width="1920" height="1140" alt="login_page" src="https://github.com/user-attachments/assets/f983a411-539b-4e70-bd90-226c1431a0cd" />


**Unified Threat Dashboard**
![SentinelTrap Dashboard]<img width="1920" height="1140" alt="working_dashboard" src="https://github.com/user-attachments/assets/0212b65b-664b-4473-8007-880174c06792" />


---

## Repository Structure

```text
SentinelTrap-Enterprise/
|
|-- app.py                          # Main Flask Application & API Routes
|-- README.md                       # Project Documentation
|-- Elevate_Labs_Capstone_Report.pdf# 2-Page Official Internship Report
|
|-- templates/
|   \-- index.html                  # Frontend Dashboard UI
|
|-- screenshots/
|   |-- login.png                   # Authentication Portal
|   \-- dashboard.png               # Unified Operations Interface
|
\-- src/
    |-- honeypot.py                 # SSH Deception Server
    \-- dashboard.py                # Analytics Generator
```

---

## Legal Disclaimer

**This tool was developed strictly for educational purposes and authorized security testing** as part of the Elevate Labs Internship Program. 

Do not use these offensive tools against targets without prior mutual consent. Unauthorized network scanning, web fuzzing, or log manipulation is illegal and strictly prohibited. The author assumes no liability for misuse or damage caused by this program.

---
<div align="center">

**Pradheepa M**  
Aspiring Cybersecurity Analyst | Python • Linux • VAPT

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pradheepa-m-051728372)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/pradheepa73)

</div>
