import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for


http_logger = logging.getLogger("http_logger")
http_logger.setLevel(logging.INFO)

http_handler = RotatingFileHandler("http_server.log", maxBytes=2000, backupCount=5)
http_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
http_handler.setFormatter(http_formatter)
http_logger.addHandler(http_handler)

def web(input_username='outhmane', input_password='password'):
    app = Flask(__name__)
    @app.route('/')

    def index():
        return render_template('web.html')
    
    @app.route('/web-admin', methods=['POST'])

    def login():
        username = request.form['username']
        password = request.form['password']

        ip = request.remote_addr

        http_logger.info(f"[{ip}] Login attempt with username: {username}")


        # response
        if username == 'outhmane' and password == 'password':
            return 'HEY STALKER'
        else:
            http_logger.info(f"[{ip}] Failed login attempt with username: {username}")
            return 'Invalid credentials', 401
        
    return app

def run_web(port=5000, username='outhmane', password='password'):
    run_web_honeypot = web(username, password)
    run_web_honeypot.run(debug=True, port=port, host='0.0.0.0')

    return run_web_honeypot


