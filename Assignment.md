# Online Message Board Client using C/C++, Java or Python

## Table of Contents
1. Project Description
2. Development Environment
3. Project Demo
4. List of Tasks
5. Project Requirements and Tutorials
6. Code Quality
7. Assessment Tool
8. Submission
9. Getting Help


## 1. Project Description
In this project, you will implement the client of an online message board system. The online message board is a client-server application where clients can **POST, GET, and DELETE** messages. The server runs on a specified port and supports four commands received from clients: POST, GET, DELETE, and QUIT.

### (1) POST Command
This command allows the client to send a message to the server. The input rules are as follows:
- The first line must be the command (i.e., POST).
- Subsequent lines are treated as part of the message content.
- The message ends with the special symbol `#`.

**Example**: If a user wants to post the message "some text!\nmore text.", the input format is:
```
POST
some text!
more text.
#
```
After receiving the message, the server will return an acknowledgment "OK".

### (2) GET Command
When the server receives this command, it will send all previously received messages to the client. The sent data includes:
- The original message content.
- The **message ID** (assigned by the server).
- The **message reception time**.
The client must print all this information on the screen. Note that the server will also include messages sent by other clients (if any).

### (3) DELETE Command
Clients can use this command to delete messages from the server by specifying message IDs (message IDs can be obtained via the GET command). The input rules are as follows:
- The first line must be the command (i.e., DELETE).
- Each subsequent line contains one message ID to be deleted.
- The operation ends with the symbol `#`.

**Example**: If a client wants to delete messages with IDs 0000, 0001, and 0002, the input format is:
```
DELETE
0001
0000
0002
#
```
- Successful deletion: The server returns "OK".
- Invalid ID(s) exist: The server returns "ERROR".

### (4) QUIT Command
This command allows the client to notify the server to close the current session:
- After receiving the command, the server returns an acknowledgment "OK".
- The server then disconnects from the client.


### Client Socket Design Example
Assume the server runs on IP address `127.0.0.1` and port `16111`. The workflow of the client socket is as follows:
1. Establish a TCP connection with the server socket.
2. Continuously prompt the user to enter commands for execution.
3. For GET and QUIT commands: Only send the command name to the server.
4. For POST and DELETE commands: Send the command name (first line) plus subsequent message content or IDs to be deleted.

The following is a typical communication scenario between the client and the server:
```
[sh-3.2$ ./MessageBoardClient 127.0.0.1 16111
Client: WRONG COMMAND
Server: ERROR-Command not understood
Client: POST
Client: some text1
Client: some text2
Client: #
Server: OK
Client: POST
Client: some text3
Client: #
Server: OK
Client: GET
Server: Happy Socket Programming
Server: MESSAGE ID:0000, RECEIVED DATETIME:15/10/2024 12:13:31
Server: some text1
Server: some text2
Server: MESSAGE ID:8001, RECEIVED DATETIME:15/10/2024 12:13:40
Server: some text3
Server: #
Client: DELETE
Client: INVALID ID
Client: #
Server: ERROR- Wrong ID
Client: DELETE
Client: 0000
Client: 0001
Client: #
Server: OK
Client: GET
Server: Happy Socket Programming
Server: #
Client: QUIT
Server: OK
```

> Note: The server program is provided and can be downloaded from the project demo files. You only need to implement the client program, which must be named `MessageBoardClient`.


## 2. Development Environment
You can choose to code the client in C/C++, Java, or Python based on your preference and familiarity. The recommended development tools for different operating systems are listed below:

### (1) Microsoft Windows OS
| Programming Language | Tool Name       | Download/Installation Instructions                                                                 |
|----------------------|----------------|----------------------------------------------------------------------------------------------------|
| C/C++                | Visual Studio  | Download link: [Visual Studio](https://visualstudio.microsoft.com/downloads/); C++ support is required (reference: [Installation Guide](https://docs.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=vs-2017)) |
| Java                 | IntelliJ IDEA  | Download link: [IntelliJ IDEA (Windows Version)](https://www.jetbrains.com/idea/download/#section=windows) |
| Python               | PyCharm        | Download link: [PyCharm (Windows Version)](https://www.jetbrains.com/pycharm/download/#section=windows) |

### (2) Linux Ubuntu OS / Mac OS X
| Programming Language | Tool Name       | Download/Installation Instructions                                                                 |
|----------------------|----------------|----------------------------------------------------------------------------------------------------|
| C/C++                | gcc/g++        | Preinstalled by default on the system; no additional download required.                             |
| Java                 | IntelliJ IDEA  | Mac Version: [IntelliJ IDEA (Mac Version)](https://www.jetbrains.com/idea/download/#section=mac); Linux Version: [IntelliJ IDEA (Linux Version)](https://www.jetbrains.com/idea/download/#section=linux) |
| Python               | PyCharm        | Mac Version: [PyCharm (Mac Version)](https://www.jetbrains.com/pycharm/download/#section=mac); Linux Version: [PyCharm (Linux Version)](https://www.jetbrains.com/pycharm/download/#section=linux) |

> Recommendation: Members of the same group should use the same operating system and development tools to avoid collaboration issues.


## 3. Project Demo
Demo programs for different operating systems are provided to demonstrate the application's workflow:
- Windows OS: Demo program (only supports Windows 10 64-bit).
- Linux OS: Demo program (developed based on Ubuntu 18 64-bit).
- Mac OS: Demo program (developed based on Mac OS High Sierra).


### 3.1 Steps to Run the Demo Program
#### (1) Start the Server Program
- Linux/Mac OS: Open the terminal and enter the command `./MessageBoardServer`.
- Windows OS: Open the Command Prompt and enter the command `MessageBoardServer.exe`.

#### (2) Start the Client Program
- Linux/Mac OS: Enter the command `./MessageBoardClient <server_ip_address> <server_port>` in the terminal (replace `<server_ip_address>` with the server's IP and `<server_port>` with the server's port).
- Windows OS: Enter the command `MessageBoardClient.exe <server_ip_address> <server_port>` in the Command Prompt (same parameter meanings as above).


### 3.2 Notes on the Server Program
1. Default Port: The server's default port is `16111`; `<server_port>` is usually set to `16111`.
2. Log Output: The server only prints logs when receiving error messages or client commands; it remains silent when there is no operation.
3. POST Response: After receiving the POST command, the server prints all stored messages.
4. Listening State: The server continues to listen for new connections even after a client disconnects.
5. Startup Method: Run the server using the command provided in "Step 1: Start the Server Program".


## 4. List of Tasks
You need to complete the following 5 core tasks to implement the client functionality:

### Task 1: Socket Initialization
- Description: Initialize and create a TCP socket to prepare for subsequent connections.

### Task 2: Initiate Connection Request
- Description:
  1. Receive the server's IP address and port number entered by the user.
  2. Initiate a connection request to the server via the initialized socket.

### Task 3: Send Commands to the Server
- Description: Process input and send data to the server based on the command type:
  - POST: Continuously receive user input until the user enters a line containing only `#` followed by a newline character `\n`.
  - GET: Directly send the "GET" command.
  - DELETE: Continuously receive message IDs to be deleted until the user enters a line containing only `#` followed by a newline character `\n`.
  - QUIT: Directly send the "QUIT" command.
  - Other Commands: Directly send the command (the server will return an error response).

### Task 4: Receive Messages from the Server
- Description: Receive the server's response and perform corresponding operations:
  - POST: If "OK" is received, print "OK" and prompt the user to enter the next command.
  - GET: Receive all messages from the server, print them on the screen, and then prompt the user to enter the next command.
  - DELETE: If "OK" is received, print "OK" (deletion successful); if "ERROR - Wrong ID" is received, print the error (deletion failed).
  - QUIT: After receiving "OK", execute "Task 5: Close the Socket".
  - Other Cases: If "ERROR - Command not understood" is received, print the error and prompt the user to re-enter a command.

### Task 5: Close the Socket
- Description: After the client sends the QUIT command and receives the server's "OK" response, close the current connection socket.


### Supplementary: Find the Server IP Address
- Linux/Mac OS: Enter the command `ifconfig` in the terminal to view network interface information.
- Windows OS: View via "Settings > Network & Internet > Network Properties".


## 5. Project Requirements and Tutorials
### 5.1 Project Tutorials
Tutorials for C/C++, Java, and Python are provided to help you start development (completing the 5 tasks above will finish the assignment):
- C/C++ Tutorial: C/C++_tutorial
- Java Tutorial: Java_tutorial
- Python Tutorial: Python_tutorial

### 5.2 Code Quality Requirements
You must follow the following coding standards. There is no unified style, but the core principles must be met:
1. **Program Decomposition**: Split the program into subroutines (or multiple source files if necessary). A 500-line program written in a single subroutine is not allowed.
2. **Comment Standards**:
   - Comments must be concise and useful (to help understand the code, not redundant content).
   - Lines from *Star Wars* or *The Hitchhiker's Guide to the Galaxy* are prohibited as comments (considered invalid comments and will result in point deductions).
   - Comments must be written in English (the university's instructional language).
3. **Variable Naming**: Variable names must have clear meanings; meaningless names like "leia" are not allowed.
4. **Global Variables**: Minimize the use of global variables (if necessary, use very few). Global variables named "temp" are prohibited.
5. **Return Value Handling**: Check the return values of all function calls and handle them appropriately (avoid ignoring errors).


## 6. Assessment Tool
### 6.1 Basic Requirements
1. The `readme.txt` file must clearly state:
   - How to compile the code.
   - How to run the code.
   - The development environment (operating system, development tools).
2. Teaching Assistants (TAs) will not fix bugs in your source code or Makefile.
3. The assignment will be deemed "unsuccessful" if:
   - No executable file can be generated.
   - The executable file cannot run normally.
   - The output format does not meet the requirements in "1. Project Description".

### 6.2 Marking Scheme
If the program runs normally and the output format is correct, marks will be awarded based on the following criteria:

| Weight | Assessment Item               | Description                                                                 |
|--------|--------------------------------|-----------------------------------------------------------------------------|
| 5%     | Socket Initialization          | Correctness of initialization logic; no errors.                            |
| 5%     | Connection Request Initiation  | Correct handling of server IP/port; correctness of connection logic.        |
| 15%    | POST Command Functionality     | Correct handling of message input; correct processing of server responses.  |
| 15%    | GET Command Functionality      | Correct command sending; correct reception and printing of messages.       |
| 15%    | DELETE Command Functionality   | Correct handling of ID input; correct processing of deletion results.       |
| 15%    | QUIT Command Functionality     | Correct command sending; correct logic for socket closure.                 |
| 10%    | Comment Standardization        | Completeness of comments; English expression; no invalid content.          |
| 10%    | Variable Naming & Program Structure | Meaningful variable names; reasonable program decomposition.             |
| 10%    | Error Handling & Return Value Check | Handling of function return values; handling of abnormal scenarios (e.g., invalid IDs). |


## 7. Submission
### 7.1 Grouping & Academic Integrity
- Grouping Rules: The assignment can be completed individually or in groups of two.
- Collaboration Requirements: High-level design discussions are allowed, but code must be implemented independently.
- Academic Integrity: Plagiarism (copying others' code or allowing others to copy your code) is considered a serious academic violation, with corresponding consequences.

### 7.2 List of Submission Files
The following files must be submitted (no missing files):
1. Source Code File: Choose the corresponding format based on the language (e.g., `.cpp`, `.c`, `.py`, `.java`).
2. `readme.txt` File: Explain how to compile the code, how to run the code, and the development environment.
3. Makefile File: Required only for C/C++ projects (used to compile the code).

### 7.3 File Naming Rules
Name files using student IDs, following these formats:
- Group of Two: `5xxxxxxx-5xxxxxxx.xxx` (two IDs connected by a hyphen; the suffix is the source code format).
- Individual: `5xxxxxxx.xxx` (one ID; the suffix is the source code format).
- Readme File: `5xxxxxxx-readme.txt` (individual) or `5xxxxxxx-5xxxxxxx-readme.txt` (group of two).

### 7.4 Submission Method & Deadline
- Submission Platform: Canvas.
- Deadline: As required by the course (**late submissions are not accepted**).


## 8. Getting Help
If you encounter programming issues, you can contact the TA via the following:
- TA Name: Bai Zhao
- Contact Email: zhao.bai@cityu-dg.edu.cn


### Copyright Notice
All content on this page (source code, documents, tutorials) is for the teaching of the CS5222 course only and is prohibited for other uses.  
Last Updated: October 2025
