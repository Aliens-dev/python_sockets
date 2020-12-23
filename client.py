import socket
import sys


HOST = input("Enter Server IP:")
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(sys)
    s.connect((HOST,PORT))
    while True:
        msg = input("Please enter Message: ")
        print(msg)
        if msg == ':q':
            s.close()
            break
        else:
            s.sendall(bytes(msg, 'utf-8'))
            data = s.recv(1024)
print('Disconnected')