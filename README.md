# PortScanner

`PortScanner` is a lightweight tool designed to facilitate port scanning by using both a server and a client component. This project allows you to scan for open ports on a server by sending data and receiving responses from a designated set of ports. It consists of a server component that listens on specified ports and a client component that connects to those ports to check their availability.

## Features

- **Port Listening Server**: The server listens on specified ports and handles incoming connections.
- **Port Scanning Client**: The client scans the specified ports on the server and sends test data to check for availability.
- **Multi-threaded**: The server uses threading to handle multiple connections concurrently.
- **Customizable**: Both the server and client allow users to define port ranges, supporting flexibility in scanning.

## Installation

### Requirements

- Python 3.7+
- `socket`, `argparse`, `logging`, `threading`, `concurrent.futures`, and `datetime` (standard Python libraries)

### Step 1: Clone the Repository

```bash
git clone https://github.com/nineking424/portscanner.git
cd portscanner
```

### **Step 2: Create Executables (Optional)**

If you prefer to create standalone executables, you can use pyinstaller. Follow these steps:

**For portlistener.py (Server)**

```bash
pyinstaller --onefile --distpath ./bin src/portlistener.py
rm -rf build portlistener.spec
```

**For portscanner.py (Client)**

```bash
pyinstaller --onefile --distpath ./bin src/portscanner.py
rm -rf build portscanner.spec
```

This will generate the executables in the ./bin directory.

## Usage

**Running the Server (Port Listener)**

The server listens on specified ports and accepts incoming connections, logging all the activity. It processes requests and responds with the details of the connection.

```bash
python src/portlistener.py <port_ranges>
```

**Example:**

```bash
python src/portlistener.py 8080,8000-8005
```

- This example starts the server listening on port 8080 and ports 8000 through 8005.

**Running the Client (Port Scanner)**

The client connects to the server’s specified IP and port range to test if the ports are open. It sends a “ping” message to each port and receives a response.

```bash
python src/portscanner.py <server_ip> <port_ranges>
```

**Example:**

```bash
python src/portscanner.py 192.168.1.10 8080,8000-8005
```

- This example scans ports 8080 and 8000-8005 on the server located at 192.168.1.10.

**Output**

The server will log connection attempts, and the client will display the results of the connection attempt to each port:

- **Server Side**: Logs details such as client IP, client port, and received messages.
- **Client Side**: Logs success or failure of connecting to each port, along with the server’s response.

**Example Output**

**Server:**

```bash
2024-08-26 12:45:23 - INFO - Server listening on 0.0.0.0:8080
2024-08-26 12:46:10 - INFO - Connection from 192.168.1.2:34567 to server's IP 192.168.1.10:8080 on port 8080
2024-08-26 12:46:11 - INFO - Received from 192.168.1.2:34567 to 192.168.1.10:8080: ping
```

**Client:**

```bash
2024-08-26 12:46:10 - INFO - Trying to connect to 192.168.1.10:8080
2024-08-26 12:46:10 - INFO - Sent message: 'ping' to 192.168.1.10:8080
2024-08-26 12:46:11 - INFO - Received response from 192.168.1.10:8080: [2024-08-26 12:46:10][192.168.1.2:34567 -> 192.168.1.10:8080] ping
```

**Stopping the Server**

To stop the server gracefully, use Ctrl+C. This will trigger a shutdown of all active connections.

## How It Works

- The **Server** (portlistener.py) binds to the specified ports and listens for incoming connections using multi-threading to handle multiple clients concurrently. It logs connection attempts and echoes back any received data.
- The **Client** (portscanner.py) attempts to connect to each port in the given range on the server’s IP address, sending a “ping” message and logging the server’s response.

### **Error Handling**

- **Port Binding Failure**: If the server fails to bind to a port (due to it being in use or unavailable), an error is logged.
- **Timeouts**: Both the server and client use timeouts to prevent indefinite blocking on network operations.

### **License**

This project is licensed under the MIT License - see the [LICENSE](https://www.notion.so/stjeong/LICENSE) file for details.

### **Contributing**

We welcome contributions! Feel free to open an issue or submit a pull request. Ensure your code follows Python best practices and includes appropriate logging.

### **Acknowledgments**

This project was developed as part of a cybersecurity learning initiative. It serves as an educational tool to demonstrate basic port scanning techniques and multi-threaded server-client architecture.

```bash
This README includes detailed information about installation, usage, and how the project works, making it easier for users to understand and get started with the `PortScanner` project. Let me know if you need further customization!
```
