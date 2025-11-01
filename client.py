#!/usr/bin/env python3
"""
Message Board Client
A TCP socket client for online message board system.
Supports POST, GET, DELETE, and QUIT commands.
"""

import socket
import sys
import argparse


class MessageBoardClient:
    """Client for message board communication with server."""

    def __init__(self, host, port, buffer_size=4096):
        """
        Initialize the message board client.

        Args:
            host: Server IP address or hostname
            port: Server port number
            buffer_size: Size of receive buffer in bytes
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.is_connected = False

    def create_socket(self):
        """
        Task 1: Initialize and create TCP socket.

        Returns:
            True if socket created successfully, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[INFO] Socket created successfully")
            return True
        except socket.error as err:
            print(f"[ERROR] Failed to create socket: {err}")
            return False

    def connect_to_server(self):
        """
        Task 2: Establish connection to server.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            print(f"[INFO] Attempting to connect to {self.host}:{self.port}")
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            print(f"[INFO] Connected to server successfully")
            return True
        except socket.error as err:
            print(f"[ERROR] Connection failed: {err}")
            return False
        except Exception as err:
            print(f"[ERROR] Unexpected error during connection: {err}")
            return False

    def send_command(self, command):
        """
        Task 3: Send command to server based on command type.

        Args:
            command: Command string (POST, GET, DELETE, QUIT, etc.)

        Returns:
            True if sent successfully, False otherwise
        """
        command = command.strip().upper()

        try:
            if command == "POST":
                return self._send_post_command()
            elif command == "GET":
                return self._send_simple_command("GET")
            elif command == "DELETE":
                return self._send_delete_command()
            elif command == "QUIT":
                return self._send_simple_command("QUIT")
            else:
                # Send unknown command and let server respond with error
                return self._send_simple_command(command)
        except Exception as err:
            print(f"[ERROR] Failed to send command: {err}")
            return False

    def _send_post_command(self):
        """
        Send POST command with message content.
        User inputs multiple lines until '#' is entered.

        Returns:
            True if sent successfully, False otherwise
        """
        print("Enter message content (end with '#' on a new line):")
        message_lines = ["POST"]

        while True:
            try:
                line = input()
                if line.strip() == "#":
                    message_lines.append("#")
                    break
                message_lines.append(line)
            except EOFError:
                print("[ERROR] Unexpected end of input")
                return False

        message = "\n".join(message_lines)
        return self._send_data(message)

    def _send_delete_command(self):
        """
        Send DELETE command with message IDs.
        User inputs message IDs until '#' is entered.

        Returns:
            True if sent successfully, False otherwise
        """
        print("Enter message IDs to delete (one per line, end with '#'):")
        delete_lines = ["DELETE"]

        while True:
            try:
                line = input()
                if line.strip() == "#":
                    delete_lines.append("#")
                    break
                delete_lines.append(line.strip())
            except EOFError:
                print("[ERROR] Unexpected end of input")
                return False

        message = "\n".join(delete_lines)
        return self._send_data(message)

    def _send_simple_command(self, command):
        """
        Send simple command without additional input.

        Args:
            command: Command string to send

        Returns:
            True if sent successfully, False otherwise
        """
        return self._send_data(command)

    def _send_data(self, data):
        """
        Send data through socket.

        Args:
            data: String data to send

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            self.socket.sendall(data.encode('utf-8'))
            return True
        except socket.error as err:
            print(f"[ERROR] Failed to send data: {err}")
            return False

    def receive_response(self, command):
        """
        Task 4: Receive and process server response.

        Args:
            command: Original command sent to server

        Returns:
            True to continue, False to quit
        """
        command = command.strip().upper()

        try:
            response = self._receive_data()

            if response is None:
                print("[ERROR] Failed to receive response from server")
                return False

            if command == "POST":
                return self._handle_post_response(response)
            elif command == "GET":
                return self._handle_get_response(response)
            elif command == "DELETE":
                return self._handle_delete_response(response)
            elif command == "QUIT":
                return self._handle_quit_response(response)
            else:
                return self._handle_error_response(response)

        except Exception as err:
            print(f"[ERROR] Error processing response: {err}")
            return False

    def _receive_data(self):
        """
        Receive data from socket.

        Returns:
            Decoded string data or None if error occurs
        """
        try:
            data = self.socket.recv(self.buffer_size)
            if not data:
                print("[INFO] Server closed the connection")
                return None
            return data.decode('utf-8')
        except socket.error as err:
            print(f"[ERROR] Failed to receive data: {err}")
            return None

    def _handle_post_response(self, response):
        """Handle response for POST command."""
        if response.strip() == "OK":
            print("OK")
            return True
        else:
            print(f"[ERROR] Unexpected response: {response}")
            return True

    def _handle_get_response(self, response):
        """Handle response for GET command."""
        print(response)
        return True

    def _handle_delete_response(self, response):
        """Handle response for DELETE command."""
        if "OK" in response:
            print("OK")
        elif "ERROR" in response:
            print(response.strip())
        else:
            print(f"[ERROR] Unexpected response: {response}")
        return True

    def _handle_quit_response(self, response):
        """Handle response for QUIT command."""
        if response.strip() == "OK":
            print("OK")
            print("[INFO] Closing connection...")
            return False
        else:
            print(f"[ERROR] Unexpected response: {response}")
            return False

    def _handle_error_response(self, response):
        """Handle error response for unknown commands."""
        print(response.strip())
        return True

    def close_socket(self):
        """
        Task 5: Close socket connection.
        """
        if self.socket:
            try:
                self.socket.close()
                print("[INFO] Socket closed successfully")
            except socket.error as err:
                print(f"[ERROR] Error closing socket: {err}")
            finally:
                self.is_connected = False
                self.socket = None

    def run(self):
        """Main client loop for interactive command input."""
        if not self.create_socket():
            return

        if not self.connect_to_server():
            self.close_socket()
            return

        print("\nAvailable commands: POST, GET, DELETE, QUIT")
        print("Enter command:")

        try:
            while self.is_connected:
                try:
                    command = input("> ").strip()

                    if not command:
                        continue

                    if not self.send_command(command):
                        break

                    if not self.receive_response(command):
                        break

                except EOFError:
                    print("\n[INFO] EOF received, sending QUIT command")
                    self.send_command("QUIT")
                    self.receive_response("QUIT")
                    break

        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
        finally:
            self.close_socket()


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Message Board Client - TCP socket client for online message board",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --host 127.0.0.1 --port 12345
  %(prog)s -H localhost -p 8080
  %(prog)s -H 192.168.1.100 -p 9000 --buffer-size 8192
        """
    )

    parser.add_argument(
        '-H', '--host',
        type=str,
        default='127.0.0.1',
        help='Server IP address or hostname'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=9090,
        help='Server port number'
    )

    parser.add_argument(
        '-b', '--buffer-size',
        type=int,
        default=4096,
        help='Receive buffer size in bytes (default: 4096)'
    )

    return parser.parse_args()


def main():
    """Main entry point for the client application."""
    args = parse_arguments()

    # Validate port number
    if not (0 < args.port < 65536):
        print(f"[ERROR] Invalid port number: {args.port}. Must be between 1 and 65535.")
        sys.exit(1)

    # Validate buffer size
    if args.buffer_size <= 0:
        print(f"[ERROR] Invalid buffer size: {args.buffer_size}. Must be positive.")
        sys.exit(1)

    # Create and run client
    client = MessageBoardClient(args.host, args.port, args.buffer_size)
    client.run()


if __name__ == "__main__":
    main()