#!/usr/bin/python3
# SMTP Username Enumeration Program.
# The program is tested on Kali/ubuntu.
# Usage: smtp_enum.py <target_ip> <wordlist file>
# unix_users.txt downloaded from https://raw.githubusercontent.com/rapid7/metasploit-framework/master/data/wordlists/unix_users.txt

__author__ = "Rajesh Kumar N"
__version__ = "1.0"

import os
import socket
import sys
if len(sys.argv) != 3:
    print("Usage: smtp_enum.py <target_ip> <wordlist file>")
    sys.exit(0)

users_wordlist = sys.argv[2]

def create_socket_connection():
    # Create a Socket
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the Server
    try:
        connect = s.connect((sys.argv[1], 25))
    except ConnectionRefusedError:
        print("SMTP port is not opened. Kindly check the port number.")
        sys.exit(1)
    except socket.gaierror:
        print("Please check your Target IP address or Internet connection.")
        sys.exit(1)
    # Receive the banner
    banner = s.recv(1024)
    print(banner)
    return s

def verify_user(s,username):
    # VRFY a user
    s.send(('VRFY ' + username + '\r\n').encode())
    result = s.recv(1024)
    print(result)

if os.path.exists(users_wordlist):
    s = create_socket_connection()

    with open(users_wordlist, 'r') as users_wordlist:
        for line in users_wordlist:
            if line.strip():
                try:
                    verify_user(s,line.strip())
                except ConnectionResetError:
                    print("Connection Reset Error occurred.")
                    s = create_socket_connection()
                    verify_user(s,line.strip())
    # Close the socket
    s.close()
else:
    print("Wordlist file does not exists.")