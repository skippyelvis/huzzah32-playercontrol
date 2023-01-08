import socket
import subprocess
import os
import glob

VIDDIR = "/home/jaa/Videos"
filelist = []

def playpause(conn):
    subprocess.run(["playerctl", "play-pause"])
    print("playpause")
    conn.sendall(bytes("playpause", "UTF-8"))

def fastforward(conn, sec=10):
    subprocess.run(["playerctl", "position", f"{sec}+"])
    print("ff")
    conn.sendall(bytes("ff", "UTF-8"))

def rewind(conn, sec=10):
    subprocess.run(["playerctl", "position", f"{sec}-"])
    print("rewind")
    conn.sendall(bytes("rewind", "UTF-8"))

def play(conn, idx):
    subprocess.run(["playerctl", "open", f"{filelist[idx]}"])
    print(f"playing {filelist[idx]}")
    conn.sendall(bytes(f"playing {filelist[idx]}", "UTF-8"))

def list_videos(conn):
    global filelist
    files = []
    files += list(glob.glob(VIDDIR + "/**/*.mp4", recursive=True))
    files += list(glob.glob(VIDDIR + "/**/*.mkv", recursive=True))
    filelist = files
    msg = ",".join(files)
    print(msg)
    conn.sendall(bytes(msg, "UTF-8"))

handlers = {
    "up": playpause,
    "down": playpause,
    "right": fastforward,
    "left": rewind,
    "sel": list_videos
}

def handle(buf, conn):
    buf = buf.decode()
    if buf in handlers:
        handlers[buf](conn)
    else:
        try:
            buf = int(buf)
            play(conn, buf)
        except:
            conn.sendall(bytes("awaiting command...", "UTF-8"))

if __name__ == "__main__":
    HOST = ""
    PORT = 5000
    TIMEOUT = None
    MAXBUF = 2048

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        conn.settimeout(TIMEOUT)
        buf = conn.recv(MAXBUF)
        resp = handle(buf, conn)
        conn.close()
