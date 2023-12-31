import threading
import socket

nickname = input("Enter a nickname: ")
if nickname == 'admin':
    password = input('enter password for admin: ')

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection was refused! You are banned")
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()