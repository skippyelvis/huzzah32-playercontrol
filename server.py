import socket
import subprocess

def playpause():
    subprocess.run(["playerctl", "play-pause"])
    print("playpause")

def fastforward(sec=10):
    subprocess.run(["playerctl", "position", f"{sec}+"])
    print("ff")

def rewind(sec=10):
    subprocess.run(["playerctl", "position", f"{sec}-"])
    print("rewind")

handlers = {
    "up": playpause,
    "down": playpause,
    "right": fastforward,
    "left": rewind,
    "sel": playpause
}

def handle(buf):
    buf = buf.decode()
    handlers[buf]()

HOST = ""
PORT = 5000
TIMEOUT = None
MAXBUF = 256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.bind((HOST, PORT))
s.listen()
print("Listening")

while True:
    conn, addr = s.accept()
    conn.settimeout(TIMEOUT)
    buf = conn.recv(MAXBUF)
    if len(buf) == 0:
        continue
    print("Received", buf, "from", addr)
    handle(buf)
    print("==============")
    conn.close()
