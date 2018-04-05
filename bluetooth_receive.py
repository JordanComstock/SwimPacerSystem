import bluetooth
import timed_LEDs


server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

while True:
    data = client_socket.recv(1024)
    data = data.decode().split(" ")

    numLaps, timeSec, timeMs = data[0], data[1], data[2]


    timed_LEDs.start_LEDs(numLaps, timeSec, timeMs)
client_socket.close()
