# lib
import logging # loggin the ip @ username and pass
from logging.handlers import RotatingFileHandler # loggin the ip @ username and pass
import socket
import threading
import paramiko

# Logging
pipe = logging.getLogger("ssh_server")
pipe.setLevel(logging.INFO) # WHAT AM I DOING?

pipe_handler = RotatingFileHandler("ssh_server.log", maxBytes=10000, backupCount=5) # file name
pipe_handler.setFormatter(logging.Formatter('%(message)s')) # ?

pipe.addHandler(pipe_handler)

# for bots commands
creds = logging.getLogger("creds_ssh_server")
creds.setLevel(logging.INFO) # WHAT AM I DOING?

creds_handler = RotatingFileHandler("creds_ssh_server.log", maxBytes=10000, backupCount=5) # file name
creds_handler.setFormatter(logging.Formatter('%(message)s')) # ?

creds.addHandler(creds_handler)

# 1. clinet:$ ssh outhmane@192.168.1.101

# building a shell

def shell(channel, ip):
    channel.send(b'outhmane$')
    command = b''
    while True:
        msg = channel.recv(1024)
        channel.send(msg)

        if not msg:
            channel.close()

        command += msg

        if msg == b'\r':
            if command.strip() == b'exit':
                response = b'\n Goodbye!'
                channel.close()
            elif command.strip() == b'pwd':
                response = b'\n' + b'\\usr\local\\' + '\r\n'
            elif command.strip() == b'whoami':
                response = b"\n" + b"outhmane" + b"\n"
            # building commands
            elif command.strip() == b'ls':
                response = b"\n" + b"file.txt" + b"\n"
            elif command.strip() == b'cat file.txt':
                response = b"\n" + b"hey this is an empty file" + b"\n"
            else:
                response = b'\n' + bytes(command.strip()) + b'\n'
        channel.send(response)
        channel.send(b'outhmane$')
        command = b''

# ssh server ??

class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.client_ip = client_ip
        self.input_username= input_username
        self.input_password = input_password

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEDED
        
    def get_allowed_auths(self):
        return "password"
    
    def check_auth_password(self, username, password):
        if self.username is not None and self.password is not None:
            if username == 'username' and password == 'password':
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True
    


"""
server = "192.168.1.101"
port = 22


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
server_socket.bind((server, port))
server_socket.listen()

def accept_connection():
    conn, addr = server_socket.accept()
    connected = True
    while connected:
        data = conn.recv(1024).decode('utf-8')
        if data.lower() == "":
            pass

def start():
    print(f"[*] SSH server is listening on {server}:{port}")
    while True:
        conn, addr = server_socket.accept()
        print(f"[+] New connection from {addr}")
        thread = threading.Thread(target=accept_connection, args=(conn, addr))
        thread.start()
        print(f"[*] Active connections: {threading.active_count() - 1}")

"""