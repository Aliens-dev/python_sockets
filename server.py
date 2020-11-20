import socket

# AF_INET => IPV4 / SOCK_STREAM => TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
port = 45000
# bind the connection to the client in this case the client is in the same machine as the server
sock.bind((hostname,port));

# start listening
sock.listen(5)
print("Started the server")
while True :
    # when connection is made get the client_socket and the client_addr
    client_socket, client_addr = sock.accept()

    print(f"Connection from address {client_addr}")
    # send the response back to the client!
    client_socket.send(bytes('Welcome to the server!', "utf-8"))


    #close the socket ( connection ) after sending back the data 

    client_socket.close()