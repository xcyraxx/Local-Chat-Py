import sys
import shutil
import threading
import errno
import socket
import readline
import base64
import hashlib
from cryptography.fernet import Fernet

HEADER_LENGTH = 10

client_socket = None
on_message_callback = None
cipher_suite = None

def _generate_key(password):
    # Determine a key from the password. 
    # In a real app we'd use a proper KDF (PBKDF2) with a salt.
    # For a simple chat, we'll hash the password to get 32 bytes.
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def connect(ip, port, username, password, on_message):
    global client_socket, on_message_callback, cipher_suite
    on_message_callback = on_message
    
    key = _generate_key(password)
    cipher_suite = Fernet(key)
    
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
    
    # Encrypt the message
    # 1. Encode text to bytes
    # 2. Encrypt bytes
    # 3. Base64 encode the encrypted bytes so it can safely pass as "utf-8" text through server
    # Note: Fernet output is already URL-safe base64, so it IS valid ascii/utf-8.
    # But let's be explicit: Fernet returns bytes.
    token = cipher_suite.encrypt(text.encode('utf-8'))
    
    # Send as normal
    message_header = f"{len(token):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + token)


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
            message_data = client_socket.recv(message_length)  # Keep as bytes first

            # Try to decrypt
            try:
                decrypted_message = cipher_suite.decrypt(message_data).decode('utf-8')
            except Exception:
                # If decryption fails, it might be a server message (plaintext) 
                # or a message from someone with a different key.
                # We'll try to decode as plain text for fallback
                try:
                    decrypted_message = message_data.decode('utf-8')
                except:
                    decrypted_message = "<Encrypted Message: Cannot Decrypt>"

            if on_message_callback:
                on_message_callback(username, decrypted_message)

        except IOError as e:
            if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                print('Reading error:', e)
                sys.exit()
            continue

        except Exception as e:
            print('Reading error:', e)
            sys.exit()


