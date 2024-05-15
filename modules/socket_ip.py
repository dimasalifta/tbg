import socket
def read_sensor_data(debug=False):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    if debug:
        print("##################################################")
        print(f"{__file__}")
        print(local_ip)
        print("##################################################")
    return local_ip
