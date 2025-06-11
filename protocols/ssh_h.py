# we need to log in the ip address, username and password of the hacker and to store on the log file
import logging
from logging.handlers import RotatingFileHandler
import paramiko
import subprocess
# emulated shell to accept commands from the user
def shell():
	while True:
		try:
			command = input("homelab> ").strip()
			if command == "pwd":
				response = '\n\usr\local' + '\n'
			
			result = subprocess.run(command, shell = True, capture_output=True, text=True)
# ssh is a secure protocol

ip_address = "192.168.1.107"
username = "outhmane"
password = "othman2004"

# connect to my server using my password

client = paramiko.client.SSHClient()

# ssh rely on encryption (public and private key)

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip_address, username=username, password=password)
_stdin, _stdout, _stderr = client.exec_command("df")
print(_stdout.read().decode())
client.close()
