#!/usr/bin/env python3
import socket
import json
from threading import Thread
import logging
import time
logging.basicConfig(level=logging.INFO)

class SocketServer:
    shutdown = False
    def __init__(self, host, port, id=None):
        self.server_address = (host, port)
        self.id = id

    def start_server(self, handler):
        self.server = Thread(target=self.run_server, args=[handler])
        self.server.start()

    def shutdown_server(self):
        self.shutdown = True
        
    def run_server(self, handler):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a timeout so we can check if we should shutdown, since .accpet() blocks forever
            s.settimeout(0.5)
            
            try:
                s.bind(self.server_address)
            except Exception as e:
                logging.error(f"Failed to bind to {self.server_address}: {e}")
                return
            s.listen()
            if self.id:
                logging.info(f"{self.id} Listening at {self.server_address}")
                
            while not self.shutdown:
                try:
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(4096) #will be much larger 
                        if data:
                            request = json.loads(data.decode('utf-8'))
                            response = handler(request)
                            conn.sendall(json.dumps(response).encode('utf-8'))
                except socket.timeout:
                    pass
        logging.info(f"{self.id} Closed")
        
    def send_data(self, target, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect(target)
                s.sendall(json.dumps(data).encode('utf-8'))
                response = self.recv_data(s)
                return json.loads(response.decode('utf-8'))
        except Exception as e:
            raise ConnectionError(f"Failed to communicate with {target}: {type(e)} {e}")            

    def recv_data(self, conn:socket.socket):
        chunks = []
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
        return b''.join(chunks)