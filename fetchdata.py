import socket,ssl

HOST = "dummyjson.com"
PORT = 443
PATH ="/products?limit=0"
context = ssl.create_default_context()

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:

    with context.wrap_socket(sock,server_hostname=HOST) as s:

        s.connect((HOST,PORT))

        s.sendall("GET {} HTTP/1.1\r\nHost: {}\r\nAccept: application/json\r\n\r\n".format(PATH,HOST).encode())

        chunks = b''
        while True:
            data = s.recv(2096)
            print(data)
            if not data: break
            chunks+=data
        
        chunks = chunks.decode(encoding="utf-8").split("\r\n\r\n")
        headers,content = chunks[0],chunks[1]

        with open("./data.json","wt") as f:
            f.write(content)

    