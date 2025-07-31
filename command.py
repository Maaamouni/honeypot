import argparse
from ssh import *
from web import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH Honeypot Command Line Interface")
    
    parser.add_argument("--host", type=str, default="localhost", help="Hostname of the SSH server")
    parser.add_argument("--ip", type=str, required=True, help="IP address of the SSH server")
    parser.add_argument("--port", type=int, default=2223, help="Port of the SSH server")
    parser.add_argument("-u", "--username", type=str, required=True, help="Username for SSH login")
    parser.add_argument("-p", "--password", type=str, required=True, help="Password for SSH login")

    parser.add_argument('-s', '--ssh', action='store_true', help="Start the SSH honeypot server")
    parser.add_argument('-w', '--web', action='store_true', help="Start the command line interface")

    args = parser.parse_args()

    try:
        if args.ssh:
            print(f"[+] Starting SSH honeypot on {args.ip}:{args.port} with username '{args.username}'")
            honeypot(args.ip, args.port, args.username, args.password)
        if args.web:
            print("[+] Starting HTTP Honeypot ...")
            if not args.username:
                username = "outhmane"
            if not args.password:
                password = "password"
            
            print(f"Port: {args.port} Username: {args.username} Password: {args.password}")
            run_web(port=args.port, username=args.username, password=args.password)
        else:
            parser.print_help()
        
    except:
        print("[-] Exiting honeypot...")