from modules.serial_connect import get_serial_connect
from modules import eudaq
from pynput.keyboard import Key, Listener, Controller
import sys
import threading

exit_signal = threading.Event() 

# def on_press(key):
#     if key == Key.esc:
#         # Set the exit_signal to stop the while loop
#         exit_signal.set()

def on_release(key):
    if key == Key.esc:
        exit_signal.set()
        return False
        
def start(*args):
    # Start a separate thread for your while loop
    while_thread = threading.Thread(target=read_serial, args=args)

    # Create a listener for key presses
    with Listener(on_release=on_release) as listener:
        print("Press the 'ESC' key to exit.")
        while_thread.start()
        listener.join()

    # Wait for the while loop thread to finish
    while_thread.join()

def read_serial(*args):
    serial = get_serial_connect()
    eudaq_on = False
    status = ""
    pos_rot = ""
    stp_rtp = ""
    output_file = []

    while not exit_signal.is_set():
        try:
            line = serial.readline().decode('utf-8').replace("\n", "").replace("\r", "")
            try:
                # print(line)
                if line != "":
                    if (line == "111" and not eudaq_on):
                        eudaq_on = True
                        output_file = open("./output.txt", 'a')
                        eudaq.run(f"{pos_rot}_{stp_rtp}_{'_'.join(args)}")
                    elif (line == "011" and eudaq_on):
                        eudaq_on = False
                        eudaq.stop(f"{pos_rot}, {stp_rtp}, {', '.join(args)}", output_file)
                    elif ('A' in line):
                        pos_rot = line.split('A')[1].split('B')[0]
                    elif ('C' in line):
                        stp_rtp = line.split('C')[1].split('D')[0]
            except:
                if (line == "011" and eudaq_on):
                    eudaq_on = False
                    eudaq.stop(f"{pos_rot}, {stp_rtp}, {', '.join(args)}", output_file)
                    
        except:
            pass

    try:
        output_file.close()
    except:
        pass
    try:
        serial.close()  # Close the serial connection when the script is interrupted``
    except:
        pass