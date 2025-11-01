#!/usr/bin/env python3
"""
Simple Test Server for Message Board Client
This is a basic server for testing the client implementation.
"""

import socket
import sys
import argparse
import datetime
from threading import Thread, Lock


class MessageStore:
    """Thread-safe message storage."""

    def __init__(self):
        self.messages = {}
        self.next_id = 0
        self.lock = Lock()

    def add_message(self, content):
        """Add a new message and return its ID."""
        with self.lock:
            msg_id = f"{self.next_id:04d}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.messages[msg_id] = {
                'id': msg_id,
                'content': content,
                'timestamp': timestamp
            }
            self.next_id += 1
            return msg_id

    def get_all_messages(self):
        """Return all messages as formatted string."""
        with self.lock:
            if not self.messages:
                return "No messages available."

            result = []
            for msg_id in sorted(self.messages.keys()):
                msg = self.messages[msg_id]
                result.append(f"ID: {msg['id']}")
                result.append(f"Time: {msg['timestamp']}")
                result.append(f"Message:\n{msg['content']}")
                result.append("-" * 40)

            return "\n".join(result)

    def delete_messages(self, msg_ids):
        """Delete messages by IDs. Return True if all valid, False otherwise."""
        with self.lock:
            all_valid = True
            for msg_id in msg_ids:
                if msg_id not in self.messages:
                    all_valid = False
                else:
                    del self.messages[msg_id]
            return all_valid


class ClientHandler(Thread):
    """Handle individual client connection."""

    def __init__(self, client_socket, client_address, message_store):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.message_store = message_store
        self.daemon = True

    def run(self):
        """Main client handling loop."""
        print(f"[INFO] Client connected: {self.client_address}")

        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break

                message = data.decode('utf-8')
                response = self.process_command(message)

                self.client_socket.sendall(response.encode('utf-8'))

                if message.strip().upper() == "QUIT":
                    break

        except Exception as err:
            print(f"[ERROR] Client {self.client_address} error: {err}")
        finally:
            self.client_socket.close()
            print(f"[INFO] Client disconnected: {self.client_address}")

    def process_command(self, message):
        """Process client command and return response."""
        lines = message.split('\n')
        command = lines[0].strip().upper()

        if command == "POST":
            return self.handle_post(lines[1:])
        elif command == "GET":
            return self.handle_get()
        elif command == "DELETE":
            return self.handle_delete(lines[1:])
        elif command == "QUIT":
            return "OK"
        else:
            return "ERROR - Command not understood"

    def handle_post(self, lines):
        """Handle POST command."""
        content_lines = []
        for line in lines:
            if line.strip() == "#":
                break
            content_lines.append(line)

        content = "\n".join(content_lines)
        msg_id = self.message_store.add_message(content)
        print(f"[INFO] Message {msg_id} posted by {self.client_address}")
        return "OK"

    def handle_get(self):
        """Handle GET command."""
        print(f"[INFO] GET request from {self.client_address}")
        return self.message_store.get_all_messages()

    def handle_delete(self, lines):
        """Handle DELETE command."""
        msg_ids = []
        for line in lines:
            if line.strip() == "#":
                break
            msg_ids.append(line.strip())

        if self.message_store.delete_messages(msg_ids):
            print(f"[INFO] Deleted messages {msg_ids} by {self.client_address}")
            return "OK"
        else:
            print(f"[WARNING] Invalid IDs in delete request from {self.client_address}")
            return "ERROR - Wrong ID"


class MessageBoardServer:
    """Simple message board server."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.message_store = MessageStore()

    def start(self):
        """Start the server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            print(f"[INFO] Server started on {self.host}:{self.port}")
            print("[INFO] Waiting for connections...")

            while True:
                client_socket, client_address = self.server_socket.accept()
                handler = ClientHandler(client_socket, client_address, self.message_store)
                handler.start()

        except KeyboardInterrupt:
            print("\n[INFO] Server shutting down...")
        except Exception as err:
            print(f"[ERROR] Server error: {err}")
        finally:
            if self.server_socket:
                self.server_socket.close()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Message Board Test Server")

    parser.add_argument(
        '-H', '--host',
        type=str,
        default='127.0.0.1',
        help='Server bind address (default: 127.0.0.1)'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=9090,
        help='Server port number'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    if not (0 < args.port < 65536):
        print(f"[ERROR] Invalid port: {args.port}")
        sys.exit(1)

    server = MessageBoardServer(args.host, args.port)
    server.start()


if __name__ == "__main__":
    main()