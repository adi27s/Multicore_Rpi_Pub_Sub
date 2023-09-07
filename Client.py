import socket

host = '192.168.234.209'  # replace with the server's IPv4 address
port = 12345  # the same port number as the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while True:
        a = input("Enter the value")
        s.sendall(a.encode('utf-8'))
