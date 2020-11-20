import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
port = 45000

sock.connect((hostname,port))

msg = sock.recv(8)

print(msg.decode('utf-8'))