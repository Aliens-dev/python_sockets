import socket 
from concurrent import futures

HOST = '127.0.0.1' 
PORT = 60000
list_threads = []

def start_conn(conn,addr):
        if(conn):
            print(f'{addr} Connected')
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"{addr} disconnected")
                    break
                else:
                    print(f"{data}")
                    conn.sendall(data)
            s.close()

with futures.ThreadPoolExecutor() as executer:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST,PORT))
            s.listen()
            conn, addr = s.accept()
            thread = executer.submit(start_conn, conn,addr)
            list_threads.append(thread)

for thread in list_threads:
    thread.join()

