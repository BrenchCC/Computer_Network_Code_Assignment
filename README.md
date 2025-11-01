MESSAGE BOARD CLIENT - Computer_Network_Code_Assignment
=====================================

AUTHOR and Assignment INFORMATION
------------------
AUTHOR: Brench
Project: Online Message Board Client
Language: Python 3
Protocol: TCP Socket Programming

DEVELOPMENT ENVIRONMENT
-----------------------
Operating System: Linux/macOS/Windows
Python Version: Python 3.6 or higher(I use Python 3.10)
Development Tools: Any text editor or IDE
Required Modules: socket, sys, argparse (all standard library)


RUNNING THE PROGRAM
-------------------
Basic usage:
    python3 message_board_client.py --host <SERVER_IP> --port <PORT>

Required arguments:
    -H, --host        Server IP address or hostname
    -p, --port        Server port number

Optional arguments:
    -b, --buffer-size Receive buffer size in bytes (default: 4096)
    -h, --help        Show help message

EXAMPLES
--------
1. Connect to local server on port 12345:
    python3 message_board_client.py --host 127.0.0.1 --port 12345

2. Connect to remote server:
    python3 message_board_client.py --host 192.168.1.100 --port 8080

3. Connect with custom buffer size:
    python3 message_board_client.py -H localhost -p 9000 -b 8192

4. Using short options:
    python3 message_board_client.py -H 127.0.0.1 -p 12345

SUPPORTED COMMANDS
------------------
Once connected, the client supports the following commands:

1. POST - Send a message to the server
   Usage:
   > POST
   Enter message content (end with '#' on a new line):
   This is my message
   More text here
   #

2. GET - Retrieve all messages from server
   Usage:
   > GET

3. DELETE - Delete messages by ID
   Usage:
   > DELETE
   Enter message IDs to delete (one per line, end with '#'):
   0001
   0002
   #

4. QUIT - Close connection and exit
   Usage:
   > QUIT

PROGRAM STRUCTURE
-----------------
The client is organized into the following components:

1. MessageBoardClient class:
   - create_socket(): Task 1 - Initialize TCP socket
   - connect_to_server(): Task 2 - Connect to server
   - send_command(): Task 3 - Send commands to server
   - receive_response(): Task 4 - Receive and process responses
   - close_socket(): Task 5 - Close socket connection

2. Helper methods:
   - _send_post_command(): Handle POST command input
   - _send_delete_command(): Handle DELETE command input
   - _send_simple_command(): Handle simple commands (GET, QUIT)
   - _send_data(): Send data through socket
   - _receive_data(): Receive data from socket
   - _handle_*_response(): Process different response types

3. Main functions:
   - parse_arguments(): Parse command line arguments
   - main(): Entry point and program initialization

ERROR HANDLING
--------------
The client handles the following error scenarios:
- Socket creation failure
- Connection failure
- Send/receive failures
- Invalid user input
- Server disconnection
- Unknown commands (forwarded to server)

EXIT CONDITIONS
---------------
The program terminates when:
1. QUIT command is successfully executed
2. Server closes the connection
3. User presses Ctrl+C (KeyboardInterrupt)
4. Critical error occurs (socket creation/connection failure)

TESTING
-------
To test the client, you need a running message board server.
Ensure the server is running before starting the client.

Test sequence:
1. Start the server on specified port
2. Run the client with correct host and port
3. Test POST command with sample message
4. Test GET command to retrieve messages
5. Test DELETE command with message IDs
6. Test QUIT command to close connection

TROUBLESHOOTING
---------------
Problem: "Connection refused"
Solution: Ensure the server is running and accepting connections

Problem: "Address already in use"
Solution: Wait a moment or use a different port

Problem: "Permission denied"
Solution: Use a port number above 1024 or run with appropriate privileges

Problem: Script not executable
Solution: Run with 'python3' command or set executable permissions

NOTES
-----
- All communication uses UTF-8 encoding
- Default buffer size is 4096 bytes (adjustable)
- The client validates port numbers (1-65535)
- Commands are case-insensitive
- Error messages are prefixed with [ERROR]
- Info messages are prefixed with [INFO]