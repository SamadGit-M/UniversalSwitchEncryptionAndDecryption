
import os
from configparser import ConfigParser
import sys
from lib.prototype import Client

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config = ConfigParser()
config.read(config_file)

# Initialize Client instance with manual IP and port
if input("Do you want to use the configuration file: ").upper() == "Y":
    STATIC_IP = config["Client"]["network_interface_1"]
    BUG_IP = config["Bug"]["network_interface_1"]
    BUG_PORT = int(config["Client"]["port"])
else:
    STATIC_IP = input("Enter the IP address you want to assign to the client: ")
    BUG_IP = input("Enter the IP address of the bug network interface: ")
    BUG_PORT = int(input("Enter the port number that you want to connect onto the bug: "))

def main():
    while True:
        client_instance = Client(STATIC_IP, BUG_IP, BUG_PORT)
        client_instance.connect_to_server()

        while True:
            try:
                message = input("Enter message: ").lower()

                if message:
                    if message == "ext":
                        encrypted_message = client_instance.encrypt_message(message.encode('ascii'), client_instance.server_public_key)
                        client_instance.client_socket.send(encrypted_message)

                        try:
                            ack = client_instance.client_socket.recv(1024)
                            ack_decoded = ack.decode("ascii", errors="ignore")
                            print(f"Server: {ack_decoded}")
                        except Exception:
                            print("Server closed connection unexpectedly.")

                        print("Connection terminated by the server.")
                        client_instance.client_socket.close()
                        print("Client disconnected.")

                        restart = input("Do you want to restart the server? (Y/N): ").strip().upper()
                        if restart == "Y":
                            break  # Restart client loop
                        else:
                            print("Exiting client.")
                            sys.exit()

                    else:
                        encrypted_message = client_instance.encrypt_message(message.encode('ascii'), client_instance.server_public_key)
                        client_instance.client_socket.send(encrypted_message)
                        response = client_instance.client_socket.recv(1024)
                        decrypted_response = client_instance.decrypt_message(response, client_instance.private_key)
                        print(f"Server: {decrypted_response}")
            except Exception as e:
                print(f"Error communicating with server: {e}")
                client_instance.client_socket.close()
                print("Client disconnected. Exiting...")
                sys.exit()

if __name__ == "__main__":
    main()
