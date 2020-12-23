import socket 
from concurrent import futures
import sys

HOST = '127.0.0.1' 
PORT = 5000
list_threads = []

def start_conn(conn,addr):
        print(f'{addr} Connected')
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"{addr} disconnected")
                break
            else:
                print(f"{data}")
                conn.sendall(data)


with futures.ThreadPoolExecutor() as executer:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST,PORT))
                s.listen()
                conn, addr = s.accept()
                if(conn):
                    thread = executer.submit(start_conn, conn,addr)
                    list_threads.append(thread)
            except socket.error:
                print('Socket failed to create')
                sys.exit()

for thread in list_threads:
    thread.join()

