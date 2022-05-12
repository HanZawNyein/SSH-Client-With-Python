import os
import platform

import warnings
from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko


class ClientSSH:
    def __init__(self, hostname, username, password, port):
        self.__hostname = hostname
        self.__username = username
        self.__password = password
        self.__client = paramiko.SSHClient()
        self.__port = port
        # add to known hosts
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.__client.connect(hostname=self.__hostname, username=self.__username, password=self.__password,
                                  port=self.__port)
            return True
        except:
            return False  # "[!] Cannot connect to the SSH Server"

    def execute_command(self, command):
        stdin, stdout, stderr = self.__client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        self.__client.close()


if __name__ == '__main__':
    default_port = 2233
    default_username = "root"
    hostname = input("Host Name : >> ").replace(" ", "")
    username = input(f"User Name : (default username is {default_username}) >> ").replace(" ", "")
    password = input("Password Name : >> ").replace(" ", "")
    port = input(f"Port : (default port is {default_port}) >> ").replace(" ", "")

    if not username:
        username = default_username

    if not port:
        port = default_port
    account = os.getlogin()
    client = ClientSSH(hostname=hostname, username=username, password=password, port=port)
    connecion_result = client.connect()
    if not connecion_result:
        print("[!] Cannot connect to the SSH Server")
    else:
        print("*" * 10)
        print(f"system : {platform.system()}")
        print(f"hostname : {platform.node()}")
        print(f"machine : {platform.machine()}")
        print(f"processor : {platform.processor()}")
        print(f"architecture : {platform.architecture()[0]}")
        print("*" * 10)
        while True:
            command = input(f"{hostname}:{port} >> ")
            print(command, "---------->")
            if command == "exit":
                client.close()
            output, error = client.execute_command(command=command)
            if error:
                print(error)
            if output:
                print(output)
