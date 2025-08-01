# 🛡️ Honeypot Project

## 📌 What Is a Honeypot?

A **honeypot** is a decoy system used in cybersecurity to attract potential attackers. Its primary purpose is **observation**—to monitor malicious behavior and understand attacker techniques without risking real assets.

> 🔍 Honeypots help capture insights such as:
>
> * Commands executed by attackers
> * Exploits they attempt to use
> * Files uploaded or downloaded

By simulating a vulnerable system, honeypots act as bait, providing security professionals with valuable intelligence.

---

## Project Approach
<img width="1920" height="1080" alt="Honeypot STEPS" src="https://github.com/user-attachments/assets/83e13842-4c2f-4184-94af-ef8dce710e80" />


## 🤖 How Do Attackers Interact With It?

* Simulates real-world behavior: accepts common shell commands like `ls`, `cat`, etc.
* Emulates services such as **SSH** and **HTTP**
* Displays a fake system banner:
  `Linux version 5.4.0 (mocked kernel version)`

This realistic behavior increases the likelihood of interaction from malicious actors, helping to gather meaningful data.

---

## 🛠️ Project Structure and Development Steps

### 1️⃣ Logger System

#### 🔐 What Do We Log?

* IP addresses of attackers
* Attempted usernames and passwords
* Uploaded files or download attempts
* Executed commands

#### 📁 Where Is It Logged?

* General SSH activity: `ssh_server.log`
* Credential attempts (bots): `creds_ssh_server.log`

#### 🎯 Why Logging Matters

* Helps **identify tools, scripts, or techniques** used by attackers
* Reveals **intentions and patterns**
* Enables security research and forensics

Logging is the **first component** to be implemented in any honeypot, as it's the core for data collection and analysis.

#### 2️⃣ SSH Server

* We use paramiko library to build a SSH server

How SSH Server works?

* Generate a server host key for the server to identify itself to clients (used in exchange)
* Handle authnetication, accept session channels and allows shell request

### 3️⃣ Client Handle

* Creates a Transport object from the raw TCP socket
* What happend: get the IP adress -> save it in the log file -> create a paramiko transport object 

### 4️⃣ Argument parser

* From the `command.py`:
* run: `python command.py --ip <ip adress> -p <password> --web` or `python command.py --ip <ip adress> -p <password> --ssh`

### 5️⃣ Web Honeypot

* Login HTML/CSS webpage that looks real but its a trap for attackers to simulate their attacks (web exploitation ..)
* We use Flask to log attacker input and ip adress
---

## 🎯 Project Scope

This project includes:

* 🧷 **SSH Honeypot**: Mimics a vulnerable SSH service with fake responses.
* 🌐 **HTML Honeypot**: A mock web interface designed to lure HTTP-based attacks.

Future improvements may include adding alert systems, real-time dashboards, or integration with threat intelligence platforms.

---

## How to work with it?

`git clone https://github.com/Maaamouni/honeypot.git`
`cd honeypot`

#### For web honeypot
`python web.py`

<img width="512" height="578" alt="login" src="https://github.com/user-attachments/assets/c8ace7ac-42d7-40da-9e24-aac53d05c031" />

### For ssh honeypot:
`python ssh.py`

#### In you CLI :
`ssh -p 2223 otman@127.0.0.1`

<img width="1142" height="425" alt="CLI" src="https://github.com/user-attachments/assets/1522127a-863f-442b-895f-58b0a88eb956" />


## ✅ Status

> This project is currently under active development.
> The best is yet to come.

---

