import socket
def read_sensor_data():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip
