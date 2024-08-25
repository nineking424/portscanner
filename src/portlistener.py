# portlistener.py: 포트 스캐너 서버
# pyinstaller --onefile --distpath ./bin src/portlistener.py
# rm -rf build portlistener.spec
import socket
import argparse
import threading
import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PortScannerServer:
    def __init__(self, port_list, max_workers=10):
        self.port_list = port_list
        self.max_workers = max_workers
        self.servers = []
        self.running = True

    def start_server(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for port in self.port_list:
                try:
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server_socket.bind(('0.0.0.0', port))
                    server_socket.listen(5)
                    server_socket.settimeout(10)  # 타임아웃 설정
                    self.servers.append(server_socket)
                    logging.info(f"Server listening on 0.0.0.0:{port}")
                    executor.submit(self.handle_port, server_socket, port)
                except socket.error as e:
                    logging.error(f"Failed to bind to {port} - {e}")
            
            # 안전한 종료를 위해 무한 루프를 유지하며 서버가 실행 중임을 유지
            while self.running:
                try:
                    signal.pause()  # 프로그램이 종료될 때까지 대기
                except KeyboardInterrupt:
                    logging.info("KeyboardInterrupt received. Shutting down server...")
                    self.stop_server()
                    break

    def handle_port(self, server_socket, listen_port):
        while self.running:
            try:
                conn, client = server_socket.accept()
                client_ip = client[0]
                client_port = client[1]

                # 클라이언트가 사용한 서버 측 IP 확인
                local_ip, local_port = conn.getsockname()

                logging.info(f"Connection from {client_ip}:{client_port} to server's IP {local_ip}:{local_port} on port {listen_port}")
                
                # 클라이언트 요청을 처리할 스레드를 실행
                threading.Thread(target=self.handle_client, args=(conn, client_ip, client_port, listen_port, local_ip)).start()
            except socket.timeout:
                continue
            except Exception as e:
                logging.error(f"Error accepting connection on port {listen_port} - {e}")
    
    def handle_client(self, conn, client_ip, client_port, listen_port, server_ip):
        try:
            conn.settimeout(5)  # 클라이언트 소켓에도 타임아웃 설정
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        logging.info(f"Connection closed by {client_ip}:{client_port}")
                        break  # 클라이언트가 연결을 종료한 경우 루프를 빠져나감

                    # 받은 데이터를 헥사 문자열로 변환
                    hex_data = data.hex()

                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    src = f'{client_ip}:{client_port}'
                    dst = f'{server_ip}:{listen_port}'

                    try:
                        # 데이터 디코딩 시도
                        decoded_data = data.decode('utf-8')
                        log_msg = f"Received from {client_ip}:{client_port} to {server_ip}:{listen_port}: {decoded_data}"
                        res_msg = f"[{current_time}][{src} -> {dst}] {decoded_data}"
                    except UnicodeDecodeError:
                        # 디코딩 실패 시 헥사 코드로 출력
                        log_msg = f"Received non-decodable data from {client_ip}:{client_port} to {server_ip}:{listen_port}: {hex_data}"
                        res_msg = f"[{current_time}][{src} -> {dst}] (hex) {hex_data}"
                        break  # 연결 종료

                    logging.info(log_msg)
                    conn.sendall(res_msg.encode())
                except socket.timeout:
                    # 타임아웃 발생 시 종료 플래그 확인
                    if not self.running:
                        break
        except socket.error as e:
            logging.error(f"Socket error with {client_ip}:{client_port} on port {listen_port} - {e}")
        finally:
            conn.close()
            logging.info(f"Connection with {client_ip}:{client_port} on port {listen_port} closed")

    def stop_server(self):
        self.running = False
        for server in self.servers:
            server.close()
        logging.info("All servers have been stopped.")

def parse_ports(port_input):
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
    parser = argparse.ArgumentParser(description="Port Scanner Server")
    parser.add_argument("ports", help="Comma separated list of ports or port ranges (e.g. 8080,8000-8005).")

    args = parser.parse_args()

    try:
        port_list = parse_ports(args.ports)
    except ValueError as e:
        logging.error(f"Invalid port range provided: {e}")
        sys.exit(1)

    # 서버 시작
    server = PortScannerServer(port_list)

    def signal_handler(sig, frame):
        logging.info("Signal received. Shutting down server...")
        server.stop_server()
        sys.exit(0)

    # 종료 시그널 처리
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        server.start_server()
    except Exception as e:
        logging.error(f"Server encountered an unexpected error: {e}")
        server.stop_server()
        sys.exit(1)