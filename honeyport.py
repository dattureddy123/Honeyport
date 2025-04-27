import socket
import subprocess
import threading

# Configuration
HONEYPOT_PORT = 8080  # Change this to the port you want to monitor
BLOCK_COMMAND = 'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}'

def block_ip(ip):
    """Blocks the attacker's IP using Windows Firewall."""
    try:
        command = BLOCK_COMMAND.format(ip=ip)
        subprocess.run(command, shell=True, check=True)
        print(f"[!] Blocked IP: {ip}")
    except Exception as e:
        print(f"[!] Error blocking IP: {e}")

def handle_connection(conn, addr):
    
    """Handles a connection attempt."""
    ip = addr[0]
    print(f"[!] Connection attempt from {ip}")

    # Log the connection
    with open("honeyport.log", "a") as log_file:
        log_file.write(f"Connection from {ip}\n")

    # Block the IP
    block_ip(ip)

    # Close connection
    conn.close()

def start_honeyport():
    """Starts the Honeyport listener."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", HONEYPOT_PORT))
    sock.listen(5)
    print(f"[+] Honeyport listening on port {HONEYPOT_PORT}...")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    start_honeyport()
