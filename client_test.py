import threading
import socket
import sys


#to recieve and send message from the server
def receive_info():
    while True:
        try:
            info_msg = client.recv(1024).decode('utf-8')
            if info_msg == 'NICK':
                client.send(codename.encode('utf-8'))
            elif info_msg == 'QUIT':
                sys.exit(2)
            else:
                print(info_msg)
        except Exception as exp:
            print('Server not responding')
            client.close()
            sys.exit(2)

def write_info():
    while True:
        info_msg = '{} {}'.format(codename, input(''))
        try:
            client.send(info_msg.encode('utf-8'))
        except:
            sys.exit(0)



codename = input("IRC is active, Enter your name: ")
if(len(codename)>11):
    print("Username cant have maximum length greater than 10 characters")
elif(len(codename.split(" "))>1):
    print("Username should not contain any spaces")
threads = []
#To start the connection
client = socket.socket()
client.connect((socket.gethostname(), 55599))

receive_thread = threading.Thread(target=receive_info)
receive_thread.start()
threads.append(receive_thread)
write_thread = threading.Thread(target=write_info)
write_thread.start()
threads.append(write_thread)
