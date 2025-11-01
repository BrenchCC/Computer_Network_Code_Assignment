# Message Board Client - User Guide

## Project File Description

- **message_board_client.py**: Main client program (submission file)
- **test_server.py**: Test server (for local testing, not required for the assignment)
- **readme.txt**: English documentation (required for the assignment)
- **USAGE_GUIDE.md**: Chinese user guide (this file)

## Quick Start

### 1. Prepare the Test Environment

First, start the test server (in one terminal window):

```bash
python3 test_server.py -p 12345
```

### 2. Run the Client

Run the client in another terminal window:

```bash
python3 message_board_client.py --host 127.0.0.1 --port 12345
```

Or use short options:

```bash
python3 message_board_client.py -H 127.0.0.1 -p 12345
```

## Detailed Command Explanation

### POST Command - Publish a Message

```
> POST
Enter message content (end with '#' on a new line):
This is the first line of the message
This is the second line
You can enter multiple lines
#
OK
```

**Notes:**
- Enter `POST` and press Enter
- Continue entering message content, which can be multi-line
- Enter `#` on a new line to finish
- The server returns `OK` to indicate success

### GET Command - Retrieve All Messages

```
> GET
ID: 0000
Time: 2025-10-21 14:30:15
Message:
This is the first line of the message
This is the second line
You can enter multiple lines
----------------------------------------
ID: 0001
Time: 2025-10-21 14:31:20
Message:
Another message
----------------------------------------
```

**Notes:**
- Simply enter `GET`
- Displays all historical messages
- Includes message ID, timestamp, and content

### DELETE Command - Delete Messages

```
> DELETE
Enter message IDs to delete (one per line, end with '#'):
0000
0001
#
OK
```

**Notes:**
- Enter `DELETE` and press Enter
- Enter one message ID per line
- Enter `#` on a new line to finish
- Returns `OK` on success, `ERROR - Wrong ID` on failure

### QUIT Command - Exit the Program

```
> QUIT
OK
[INFO] Closing connection...
[INFO] Socket closed successfully
```

**Notes:**
- Simply enter `QUIT`
- Automatically closes the connection after server confirmation

## Command-Line Arguments Explanation

### Required Parameters

- `-H, --host`: Server IP address or hostname
- `-p, --port`: Server port number

### Optional Parameters

- `-b, --buffer-size`: Receive buffer size (default: 4096 bytes)
- `-h, --help`: Display help information

### Usage Examples

1. **Connect to a local server:**
   ```bash
   python3 message_board_client.py -H 127.0.0.1 -p 12345
   ```

2. **Connect to a remote server:**
   ```bash
   python3 message_board_client.py -H 192.168.1.100 -p 8080
   ```

3. **Use a custom buffer:**
   ```bash
   python3 message_board_client.py -H localhost -p 9000 -b 8192
   ```

4. **View help:**
   ```bash
   python3 message_board_client.py --help
   ```

## Code Structure Explanation

### Implementation of Five Core Tasks

#### Task 1: Socket Initialization
```python
def create_socket(self):
    """Initialize and create TCP socket."""
```
- Create a TCP socket
- Error handling and logging

#### Task 2: Initiate Connection Request
```python
def connect_to_server(self):
    """Establish connection to server."""
```
- Use user-provided host and port
- Establish a TCP connection
- Handle connection failure cases

#### Task 3: Send Commands to Server
```python
def send_command(self, command):
    """Send command to server based on command type."""
```
- Handle different command types (POST, GET, DELETE, QUIT)
- POST and DELETE require multi-line input
- GET and QUIT are sent directly

#### Task 4: Receive Server Messages
```python
def receive_response(self, command):
    """Receive and process server response."""
```
- Process different responses based on command type
- POST: Display OK
- GET: Display all messages
- DELETE: Display OK or ERROR
- QUIT: Close the connection

#### Task 5: Close the Socket
```python
def close_socket(self):
    """Close socket connection."""
```
- Executed after the QUIT command
- Clean up resources
- Error handling

## Testing Steps

### Complete Test Flow

1. **Start the server:**
   ```bash
   python3 test_server.py -p 12345
   ```

2. **Start the client:**
   ```bash
   python3 message_board_client.py -H 127.0.0.1 -p 12345
   ```

3. **Test the POST command**