import ssl
from socket import *
import base64

username = ''  # my account information is removed.
password = ''  # IMPORTANT NOTE!!!!!!!!!!: PLEASE REMOVE THIS FIELD WHEN YOU SUBMIT!!!!!

subject = 'Computer Network Assignment2 - Email Client'
from_ = ''  # my account information is removed.
to_ = ''  # my account information is removed.
content = 'It is so hard for me!!!'

# Message to send
endmsg = '\r\n.\r\n'


def get_ip():
    ip = gethostbyname(gethostname())
    if ip == "127.0.0.1" or ip == "localhost":
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        ip = s.getsockname()[0]
        s.close()
    return ip


def show(t, s):
    print(f"{t}: b{repr(s)}")


def recv_print(_sock, size=1024):
    show("reply", _sock.recv(size).decode())


def send_print(_sock, msg):
    show("send", msg)
    _sock.send(msg.encode())


# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.office365.com'
port = 587

# 1. Establish a TCP connection with a mail server [2pt]
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((mailserver, port))
recv_print(sock)

# 2. Dialogue with the mail server using the SMTP protocol. [2pt]
send_print(sock, f"HELO {get_ip()}\r\n")
recv_print(sock)

# 3. Login using SMTP authentication using your postech account. [5pt]

# HINT: Send STARTTLS
send_print(sock, "STARTTLS\r\n")
recv_print(sock)

# HINT: Wrap socket using ssl.PROTOCOL_SSLv23
wrap_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)

# HINT: Use base64.b64encode for the username and password
auth_username_str = base64.b64encode(username.encode()).decode('UTF-8')
auth_password_str = base64.b64encode(password.encode()).decode("UTF-8")

# HINT: Send EHLO
send_print(wrap_sock, f"ehlo {get_ip()}\r\n")
recv_print(wrap_sock)

send_print(wrap_sock, f"AUTH LOGIN {auth_username_str}\r\n")
recv_print(wrap_sock)

send_print(wrap_sock, f"{auth_password_str}\r\n")
recv_print(wrap_sock)

# 4. Send a e-mail to your POSTECH mailbox. [5pt]
send_print(wrap_sock, f"mail FROM:<{from_}>\r\n")
recv_print(wrap_sock)

send_print(wrap_sock, f"rcpt TO:<{to_}>\r\n")
recv_print(wrap_sock)

send_print(wrap_sock, "data\r\n")
recv_print(wrap_sock)

mail_content = f"Subject: {subject}\r\nFrom: {from_}\r\nTo: {to_}\r\nContent-Type: text/plain;charset=\"utf-8\"\r\nContent-Transfer-Encoding: 7bit\r\nMIME-Version: 1.0\r\n\r\n{content}{endmsg}"

send_print(wrap_sock, mail_content)
recv_print(wrap_sock)

# 5. Destroy the TCP connection [2pt]
send_print(wrap_sock, "quit\r\n")
recv_print(wrap_sock)

wrap_sock.close()
sock.close()
