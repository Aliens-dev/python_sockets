import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
port = 45000

sock.connect((hostname,port))

full_msg = ''

while True:
    msg = sock.recv(8)
    if len(msg) <= 0:
        break
    full_msg += msg.decode('utf-8')


print(full_msg)  