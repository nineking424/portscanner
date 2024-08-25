# portscanner.py: 포트 스캐너 클라이언트
# pyinstaller --onefile --distpath ./bin src/portscanner.py
# rm -rf build portscanner.spec
import socket
import argparse
import logging
import sys

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PortScannerClient:
    def __init__(self, server_ip, port_list):
        self.server_ip = server_ip
        self.port_list = port_list
        self.message = "ping"  # 메시지는 ping으로 고정

    def run(self):
        for port in self.port_list:
            self.scan_port(port)

    def scan_port(self, port):
        try:
            # 클라이언트 소켓 생성 및 서버 연결
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                logging.info(f"Trying to connect to {self.server_ip}:{port}")
                client_socket.connect((self.server_ip, port))

                # 메시지 전송
                client_socket.sendall(self.message.encode('utf-8'))
                logging.info(f"Sent message: '{self.message}' to {self.server_ip}:{port}")

                # 서버로부터 응답 수신
                response = client_socket.recv(1024)
                logging.info(f"Received response from {self.server_ip}:{port}: {response.decode('utf-8')}")

        except (socket.timeout, socket.error) as e:
            logging.error(f"Failed to connect to {self.server_ip}:{port} - {e}")

def parse_ports(port_input):
    """복수의 포트 또는 범위를 받아 리스트로 변환"""
    port_list = []
    for port_range in port_input.split(','):
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            if start < 1 or end > 65535 or start > end:
                raise ValueError("Port numbers must be between 1 and 65535 and start must be less than or equal to end.")
            port_list.extend(range(start, end + 1))
        else:
            port = int(port_range)
            if port < 1 or port > 65535:
                raise ValueError("Port number must be between 1 and 65535.")
            port_list.append(port)
    return port_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scanner Client")
    parser.add_argument("server_ip", help="The IP address of the server")
    parser.add_argument("ports", help="Comma separated list of ports or port ranges (e.g. 8080,8000-8005).")

    args = parser.parse_args()
    server_ip = args.server_ip

    try:
        port_list = parse_ports(args.ports)
    except ValueError as e:
        logging.error(f"Invalid port range provided: {e}")
        sys.exit(1)

    # 포트 스캐너 클라이언트 실행
    scanner = PortScannerClient(server_ip, port_list)
    scanner.run()