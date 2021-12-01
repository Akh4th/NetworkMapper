from socket import *
import time
import ipaddress
global record


record = input("Would you like to record the scanning ?\n[Yes/No] : ")
if record.upper() == "YES":
    record = True
elif record.upper() == "NO":
    record = False
else:
    record = False


def rec2(number):
    file = open('NetMap.txt', 'a')
    file.write(f"Port number {number} is opened !")
    file.close()


def rec():
    file = open('NetMap.txt', 'a')
    file.write(f"Scanning started at : {tim}\nScanning the target {ip} in range of {portA}-{portB}\n")
    file.close()


while True:
    try:
        tim = time.time()
        print("Hello user, type 'done' whenever you want to quit the program")
        ip = input("Enter the IP Address you'd like to scan : ")
        print("Please enter ports range\n")
        try:
            portA = int(input("Starts with : "))
            portB = int(input("Ends with : "))
            while portA < 0:
                portA = input("Port number has to be positive number.")
            while portB < 0:
                portB = input("Port number has to be positive number.")
        except ValueError:
            print("Port has to be a number !")
            continue
        if ipaddress.ip_address(ip):
            try:
                if record:
                    rec()
                print(f"Scanning the target {ip} in range of {portA}-{portB}\n")
                for i in range(portA, portB):
                    soc = socket(AF_INET, SOCK_STREAM)
                    con = soc.connect_ex((ip, i))
                    if (con == 0):
                        print(f"Port number {i} is opened !")
                        if record:
                            rec2(i)
                    soc.close()
            except ipaddress.AddressValueError:
                print("The IP Address is not responding.\nPlease try again.")
        elif ip.upper() == 'DONE':
            print("Thank you for using.\nCya next time.")
            break
    except KeyboardInterrupt:
        print("Keyboard interrupt detected !\nABORTING !!!")
        break


