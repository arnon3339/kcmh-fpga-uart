import serial
import serial.tools.list_ports as listports

def get_port(device):
    device_SNR = {"zaber": "AL0393XP", "fpga": "210183B5A8D0"}
    ports = listports.comports()
    # device = "fpga"
    # print(ports)
    # for p in ports:
    #     print(p.device)
    for port, desc, hwid in sorted(ports):
        if device_SNR[device] in hwid:
            # print("{}: {} [{}]".format(port, desc, hwid))
            return port
    raise ConnectionError
        
# print(get_port())      
def get_serial_connect():
    serial_number = "/dev/ttyUSB1"
    baud_rate = 9600
    # serial_port = get_port(serial_number)
    ser = serial.Serial(serial_number, baud_rate)
    return ser

# get_port("")