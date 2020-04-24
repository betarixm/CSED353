import ssl
from socket import *
import base64

username = 'mzg00@postech.ac.kr'
password = ''  # IMPORTANT NOTE!!!!!!!!!!: PLEASE REMOVE THIS FIELD WHEN YOU SUBMIT!!!!!

subject = 'Computer Network Assignment2 - Email Client'
from_ = 'mzg00@postech.ac.kr'
to_ = 'refstd@postech.ac.kr'
content = 'It is so hard for me!!!'

# Message to send
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.office365.com'
port = 587

# 1. Establish a TCP connection with a mail server [2pt]
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((mailserver, port))
recv = sock.recv(1024).decode()
print(recv)

# 2. Dialogue with the mail server using the SMTP protocol. [2pt]
sock.send(b"HELO smtp.office365.com\r\n")
recv = sock.recv(1024).decode()
print(recv)

# 3. Login using SMTP authentication using your postech account. [5pt]

# HINT: Send STARTTLS
sock.send(b"STARTTLS\r\n")
recv = sock.recv(1024).decode()
print(recv)
# HINT: Wrap socket using ssl.PROTOCOL_SSLv23
wrap_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
# HINT: Use base64.b64encode for the username and password
auth_str = f"AUTH LOGIN {base64.b64encode(username.encode()).decode('UTF-8')}\r\n".encode()
# HINT: Send EHLO
wrap_sock.send(b"ehlo [141.223.176.184]\r\n")
recv = wrap_sock.recv(1024).decode()
print(recv)

wrap_sock.send(auth_str)
recv = wrap_sock.recv(1024).decode()
print(recv)

wrap_sock.send((base64.b64encode(password.encode()).decode("UTF-8") + "\r\n").encode())
recv = wrap_sock.recv(1024).decode()
print(recv)

# 4. Send a e-mail to your POSTECH mailbox. [5pt]
wrap_sock.send(f"mail FROM:<{from_}>\r\n".encode())
recv = wrap_sock.recv(1024).decode()
print(recv)

wrap_sock.send(f"rcpt TO:<{to_}>\r\n".encode())
recv = wrap_sock.recv(1024).decode()
print(recv)

wrap_sock.send("data\r\n".encode())
recv = wrap_sock.recv(1024).decode()
print(recv)

mail_content = f"Subject: {subject}\r\nFrom: {from_}\r\nTo: {to_}\r\nContent-Type: text/plain; charset=\"utf-8\"\r\nContent-Transfer-Encoding: 7bit\r\nMIME-Version: 1.0\r\n\r\n{content}{endmsg}".encode()

wrap_sock.send(mail_content)
recv = wrap_sock.recv(1024).decode()
print(recv)

# 5. Destroy the TCP connection [2pt]
wrap_sock.send("quit\r\n".encode())
recv = wrap_sock.recv(1024).decode()
print(recv)