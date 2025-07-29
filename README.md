# Honeypot
## What is a honeypot?
A honeypot in cybersecurity it refers to a decoy system designed to attract cyber attackers and gather information about their methods and intentions.

->  honeypot main purspose is "OBSERVATION", you need to see how attackers behave (what commands they run, what exploits they use and what files they upload)

## how does hackers ... ?
-  honeypot is like a real system, you can write commands like ls,cat and so on
- It responds to SSH, telnet, HTTP...
- It gives a fake banner (Linux version 5.4.0)

## Project's steps:
### 1. Loggers:

What to log?
- Ip addres
- Username 
- Password

where to log? ssh_server.log
for bots -> cres_ssh_server


- Logs allows you to :
    Identify the tools or exploits used and understand attackers intentions
- Logs is the first things that must be implemented to log the data
- What to log : login attempts - ip addresses - files uploads and downloads and so on

## What this project about?
- SSH honeypot
- HTML honeypot
