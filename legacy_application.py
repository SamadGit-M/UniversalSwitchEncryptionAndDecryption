
import os
import socket
import sys
import threading
from configparser import ConfigParser

def start_server():
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = ConfigParser()
    config.read(config_file)

    DEBUG = True if input("Debugging (Y/N): ").upper() == 'Y' else False

    if input("Do you want to use the configuration file: ").upper() == "Y":
        STATIC_IP = config["Legacy_Application"]["network_interface_1"]
        PORT = int(config["Legacy_Application"]["port"])
    else:
        STATIC_IP = input("Enter the IP address you want to assign: ")
        PORT = int(input("Enter the port number the server should listen on: "))

    client_list = []
    DATA = {
        "data": "Aditya , Samad , Varun , Ankit",
        "sih": "Sher Server"
    }

    def handle_client(client, address, server_socket):
        print(f"{client} Connected from {address}")
        client_list.append(client)

        while True:
            try:
                message = client.recv(1024).decode("ascii")

                if not message:
                    break

                if DEBUG:
                    print("\n" + "=" * 50)
                    print(f"Received PT response from {address}: \n{message}")
                    print("=" * 50)

                if message == "ser":
                    client.send(DATA["sih"].encode("ascii"))

                elif message == "own":
                    client.send(DATA["data"].encode("ascii"))

                elif message == "ext":
                    client_list.remove(client)
                    client.send(message.encode("ascii"))
                    print(f"{client} disconnected!")
                    client.close()
                    print("Closing server socket...")
                    server_socket.close()
                    print("Terminating legacy application server...")
                    return "TERMINATE"

                else:
                    client.send("Message transfer successfully".encode("ascii"))

            except Exception as e:
                print(f"Error with client {address}: {e}")
                break

        client.close()
        return "CONTINUE"

    def accept_connections():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((STATIC_IP, PORT))
        server_socket.listen()

        print("Legacy Application Server started and listening...")

        while True:
            try:
                client, address = server_socket.accept()
                result = handle_client(client, address, server_socket)
                if result == "TERMINATE":
                    return  # Exit the server cleanly
            except OSError:
                break  # Socket was closed, exit gracefully

    accept_connections()

if __name__ == "__main__":
    while True:
        start_server()
        restart = input("Do you want to restart the server? (Y/N): ").strip().upper()
        if restart != "Y":
            print("Server will not restart. Exiting...")
            break
