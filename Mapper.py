import argparse
import socket
import socket as s
from socket import *
import ipaddress

ports = []

p = argparse.ArgumentParser(description="Port Scanner !\nSeparate hosts by ',' or '-' in case of ip range")
g = p.add_mutually_exclusive_group()

p.add_argument("host", help="IP Address to search", nargs='*', type=str)
p.add_argument("-Gv", "--get_version", action="store_true", help="Get service's version")
p.add_argument("-O", "--Output", help="Prints output into a file")

g.add_argument("-P", "--ports", type=int, help="Ports number range, default is 1000.", default=1000)
g.add_argument("-p", "--port", type=int, help="Specific port number.")

args = p.parse_args()


def scans(port, IP):
    ports.clear()
    for i in range(port + 1):
        per = round((i * 100) / port, 2)
        print(f"\rChecking:\t{IP}:{i}/{port}\tProcess:\t{per}%", end="")
        soc = socket(AF_INET, SOCK_STREAM)
        con = soc.connect_ex((IP, i))
        if con == 0:
            if args.get_version:
                if args.output:
                    with open(args.output, "w+") as file:
                        file.write(f"Port number {i} is ON ! \nVersion : {ver(i, IP)}")
                        file.close()
                    ports.append(f"Port number {i} is ON ! \nVersion : {ver(i, IP)}")
                else:
                    ports.append(f"Port number {i} is ON ! \nVersion : {ver(i, IP)}")
            else:
                if args.output:
                    with open(args.output, "w+") as file:
                        file.write(f"Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
                        file.close()
                    ports.append(f"Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
                else:
                    ports.append(f"Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
    soc.close()
    print("\n")


def scan(port, IP):
    soc = socket(AF_INET, SOCK_STREAM)
    con = soc.connect_ex((IP, port))
    if con == 0:
        if args.get_version:
            if args.output:
                with open(args.output, "w+") as file:
                    file.write(f"Port number {port} is ON ! \nVersion : {ver(service=args.port, IP=args.host)}")
                    file.close()
                return f"Port number {port} is ON ! \nVersion : {ver(service=args.port, IP=args.host)}"
            else:
                return f"Port number {port} is ON ! \nVersion : {ver(service=args.port, IP=args.host)}"
        else:
            if args.output:
                with open(args.output, "w+") as file:
                    file.write(f"Port number {port} is ON ! \nVersion : {s.getservbyport(port, 'tcp')}")
                    file.close()
                return f"Port number {port} is ON ! \nVersion : {s.getservbyport(port, 'tcp')}"
            else:
                return f"Port number {port} is ON ! \nVersion : {s.getservbyport(port, 'tcp')}"
    else:
        return f"Port number {port} is OFF !"


def ver(service, IP):
    try:
        x = s.socket()
        x.connect((IP, service))
        if service == 80:
            y = "GET / HTTP/1.0\r\n\r\n"
            x.send(y.encode())
            return x.recv(1024).decode().split("\n")[0]
        else:
            return x.recv(1024).decode()
    except Exception as e:
        return f"Error while checking service number {service} \nError : {e}"


if __name__ == "__main__":
    try:
        if len(args.host) == 1:
            try:
                ipaddress.IPv4Address(args.host[0])
                # Single Port
                if args.port:
                    print(scan(port=args.port, IP=str(args.host[0])))
                # Ports range
                else:
                    scans(port=args.ports, IP=str(args.host[0]))
                    for i in ports:
                        print(i)
            except ipaddress.AddressValueError:
                if "-" in args.host[0]:
                    ranges = args.host[0].split(".")[-1:].pop().split("-")
                    for address in range(int(ranges[0]), int(ranges[1]) + 1):
                        ip = args.host[0].split(".")[0] + "." + args.host[0].split(".")[1] + "." + \
                             args.host[0].split(".")[
                                 2] + "." + str(address)
                        if ipaddress.IPv4Address(ip):
                            if args.port:
                                print(scan(port=args.port, IP=ip))
                            elif args.ports:
                                scans(port=args.ports, IP=ip)
                                for i in ports:
                                    print(i)
                        else:
                            raise ipaddress.AddressValueError
        elif "," in args.host:
            for ip in args.host:
                if ip == ",":
                    continue
                elif ipaddress.IPv4Address(ip):
                    if args.port:
                        print(scan(port=args.port, IP=ip))
                    elif args.ports:
                        scans(port=args.ports, IP=ip)
                        for i in ports:
                            print(i)
                else:
                    raise ipaddress.AddressValueError
    # Wrong IP Address
    except ValueError:
        print("Use IP Address only !")
