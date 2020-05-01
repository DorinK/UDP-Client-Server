from socket import socket, AF_INET, SOCK_DGRAM
import sys

""""""""""""""""""""""""""
    # Dorin Keshales
      # Almog Lev
""""""""""""""""""""""""""

# Receive arguments of IP and port of the server from command line.
server_ip = str(sys.argv[1])
server_port = int(sys.argv[2])

s = socket(AF_INET, SOCK_DGRAM)

msg = ''

# As long as the client still wants to be in the chat.
while not msg == '4':
    msg = input()
    s.sendto(msg.encode(), (server_ip, server_port))
    data, sender_info = s.recvfrom(2048)

    # If the data received from the server is not empty.
    if len(data.decode()) != 0:
        print(data.decode())

    # If the user asked to leave the group before joining the group then client won't quit yet.
    if data.decode() == "Illegal request" and msg == '4':
        msg = '0'

s.close()
