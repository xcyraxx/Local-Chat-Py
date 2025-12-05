import sys
import shutil
import threading
import errno
import socket
import readline

HEADER_LENGTH = 10

client_socket = None
on_message_callback = None

def connect(ip, port, username, on_message):
	global client_socket, on_message_callback
	on_message_callback = on_message
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ip, port))
	client_socket.setblocking(False)

	username = username.encode('utf-8')
	username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(username_header + username)
	
	recv_thread = threading.Thread(target=rcv_msg, daemon=True)
	recv_thread.start()

def send_msg(text):
	if not text or client_socket is None:
		return
	
	message_bytes = text.encode('utf-8')
	message_header = f"{len(message_bytes):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(message_header + message_bytes)



def rcv_msg():
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            if on_message_callback:
            	on_message_callback(username, message)

        except IOError as e:
            if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                print('Reading error:', e)
                sys.exit()
            continue

        except Exception as e:
            print('Reading error:', e)
            sys.exit()


