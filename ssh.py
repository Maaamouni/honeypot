# lib
import logging 
from logging.handlers import RotatingFileHandler 
import socket
import threading
import paramiko

SSH_BANNER = "SSH-2.0-OpenSSH_7.9\r\n" # fake banner
host_key = paramiko.RSAKey(filename='server.key')

# 1.Logging
logger = logging.getLogger("ssh_server")
logger.setLevel(logging.INFO) 

pipe_handler = RotatingFileHandler("ssh_server.log", maxBytes=10000, backupCount=5)
formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
pipe_handler.setFormatter(formater) 

logger.addHandler(pipe_handler)

# for bots commands
creds = logging.getLogger("creds_ssh_server")
creds.setLevel(logging.INFO) 

creds_handler = RotatingFileHandler("creds_ssh_server.log", maxBytes=10000, backupCount=5) 
creds_handler.setFormatter(formater) 

creds.addHandler(creds_handler)

# 1. clinet:$ ssh outhmane@192.168.1.101

# 2.building a shell

def shell(channel, ip):
    
    prompt = b'outhmane$ '
    channel.send(b'\nWelcome to the SSH honeypot!\n')
    channel.send(prompt)

    command = b''

    while True:
        try:
            msg = channel.recv(1024)

            if not msg:
                break
            
            command += msg

            if msg in [b'\r', b'\n']:
                stripped_cmd = command.strip()
                #if stripped_cmd:
                # logger.info(f"[{ip}] Command : {stripped_cmd}")
                # creds.info(f"[{ip}] Command : {stripped_cmd}")
            
                if stripped_cmd == b'exit':
                    channel.send(b'\nGoodbye!\n')
                    channel.close()

                elif stripped_cmd == b'pwd':
                    response = b'\n/usr/local/\n'
                
                elif stripped_cmd == b'whoami':
                    response = b"\nouthmane\n"
                # building commands
                
                elif stripped_cmd == b'ls':
                    response = b"\nfile.txt\n" 

                elif stripped_cmd == b'help':
                    response = b"\nAvailable commands:\n - pwd \n - whoami \n - ls \n - cat file.txt \n - help \n - exit\n" 
                
                elif stripped_cmd == b'cat file.txt':
                    response = b"\nhey this is an empty file\n"
                
                else:
                    response = b'\nCommand not found: ' + stripped_cmd + b'\n'
                
                channel.send(response)
                channel.send(prompt)
                command = b''
            
            else:
                command += msg

        except Exception as e:
            #logger.error(f"Error processing command from {ip}: {e}")
            channel.send(b'\nError: ' + str(e).encode() + b'\n')
            break

    channel.close()

class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
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
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True
    
def client_handle(client,addr,username,password):
    client_ip = addr[0]
    print(f"[+] Connection from {client_ip}")
    try:
        
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, input_username=username, input_password=password)

        transport.add_server_key(host_key)
        transport.start_server(server=server)

        channel = transport.accept(100)

        if channel is None:
            print(f"[-] Failed to open channel from {client_ip}")
            
        standard_banner = "Welcome to the CLI!\n"
        channel.send(standard_banner)
        shell(channel, client_ip)
        
    except Exception as error:
        print("Error occurred:")
        print(error)
        
    finally:
        try:
            transport.close()
        except Exception as e:
            print("Error occurred while closing transport:")
            print(e)
        finally:
            client.close()

def honeypot(ip_add, port, username, password, tarpit):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_add, port))
    sock.listen(100)
    print(f"[*] Listening for connections on {ip_add}:{port}")

    while True:
        try:
            client, addr = sock.accept()
            print(f"[+] Accepted connection from {addr}")
            thread = threading.Thread(target=client_handle, args=(client, addr, username, password, tarpit))
            thread.start()

        except Exception as e:
            print("Error occurred:")
            print(e)



honeypot('127.0.0.1', 2223, 'otman','12345678', tarpit=False)
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