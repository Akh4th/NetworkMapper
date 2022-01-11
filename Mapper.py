import socket as s
from socket import *
import ipaddress, os, argparse

ports = []
OSs = ["Ubuntu", "Unix", "Windows"]

# Arguments Parser
p = argparse.ArgumentParser(description="Python Port Scanner by Akh4th !", epilog="Host specification : ['10.0.0.1', '10.0.0.1-3', '10.0.0.1 , 10.0.0.2']", usage="Mapper.py {host specification} [--port/s PORTS] [-O output_file] [-GO] [-v] [-Gv] [-Ch]")
p.add_argument("host", help="IP Address to search", nargs='*', type=str)
p.add_argument("-O", "--Output", help="Prints output into a file", metavar="")
p.add_argument("-v", "--verbose", help="Prints process verbosely", action="store_true")
p.add_argument("-Gv", "--get_version", action="store_true", help="Get service's version")
p.add_argument("-Ch", "--check_host", help="Ping host to check if alive", action="store_true")
p.add_argument("-GO", "--get_os", help="Estimated host's Operation System", action="store_true")
p.add_argument("-Fs", "--fast_scan", help="Scan fewer ports then default.", action="store_true")
# Ports group
g = p.add_mutually_exclusive_group()
g.add_argument("-P", "--ports", type=int, help="Ports number range, default is 1000.", metavar="")
g.add_argument("-p", "--port", type=int, help="Specific port number.", metavar="")
# Parse the arguments
args = p.parse_args()


# Trying to get Operation System
def get_os(IP):
    x = s.socket()
    for i in range(1000):
        if args.verbose:
            print("\rGetting Operation System..." + str(round(((i * 100) / 1000), 2)) + "%")
        try:
            x.connect((IP, i))
            if i == 80:
                y = "GET / HTTP/1.0\r\n\r\n"
                x.send(y.encode())
                answer = x.recv(1024).decode()
            else:
                answer = x.recv(1024).decode()
            for name in OSs:
                if name in answer:
                    return name
                else:
                    continue
        except OSError:
            continue
    return "Unable to detect !"


# Check if IP is alive
def is_up(IP):
    if args.verbose:
        print(f"Checking if {IP} is alive...")
    if os.system(f"ping -c 1 {IP} > /dev/null") == 0:
        print(f"{IP} : Host is up !")
        return True
    else:
        print(f"{IP} : Host is down !")
        return False


# Scanning multiply ports
def scans(port, IP):
    ports.clear()
    for i in range(port + 1):
        per = round((i * 100) / port, 2)
        if args.verbose:
            print(f"\r{IP}:{i}/{port} processed : {per}%", end=" ")
        soc = socket(AF_INET, SOCK_STREAM)
        con = soc.connect_ex((IP, i))
        if con == 0:
            if args.get_version:
                if args.Output:
                    with open(args.Output, "w+") as file:
                        file.write(f"{IP} : Port number {i} is ON ! \nVersion : {ver(i, IP)}")
                        file.close()
                    ports.append(f"{IP} : Port number {i} is ON ! \nVersion : {ver(i, IP)}")
                else:
                    ports.append(f"{IP} : Port number {i} is ON ! \nVersion : {ver(i, IP)}")
            else:
                if args.Output:
                    with open(args.Output, "w+") as file:
                        file.write(f"{IP} : Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
                        file.close()
                    ports.append(f"{IP} : Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
                else:
                    ports.append(f"{IP} : Port number {i} is ON ! \nService : ({s.getservbyport(i)})")
    print("\n")


# Scanning a single port
def scan(port, IP):
    soc = socket(AF_INET, SOCK_STREAM)
    con = soc.connect_ex((IP, port))
    if con == 0:
        if args.get_version:
            if args.Output:
                with open(args.Output, "w+") as file:
                    file.write(f"{IP} : Port number {port} is ON ! \nService Version : {ver(service=args.port, IP=args.host[0])}")
                    file.close()
                return f"{IP} : Port number {port} is ON ! \nService Version : {ver(service=args.port, IP=args.host[0])}"
            else:
                return f"{IP} : Port number {port} is ON ! \nService Version : {ver(service=args.port, IP=args.host[0])}"
        else:
            if args.Output:
                with open(args.Output, "w+") as file:
                    file.write(f"Port number {port} is ON ! \nService : {s.getservbyport(port, 'tcp')}")
                    file.close()
                return f"{IP} : Port number {port} is ON ! \nService : {s.getservbyport(port, 'tcp')}"
            else:
                return f"{IP} : Port number {port} is ON ! \nService : {s.getservbyport(port, 'tcp')}"
    else:
        return f"{IP} : Port number {port} is OFF !"


# Getting service version
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
                    if args.check_host:
                        if not is_up(args.host[0]):
                            quit()
                    if args.get_os:
                        print(args.host[0] + "'s Estimated Operation System : " + get_os(args.host[0]))
                    print(scan(port=args.port, IP=str(args.host[0])))
                # Ports range
                elif args.ports:
                    if args.check_host:
                        if not is_up(args.host[0]):
                            quit()
                    if args.get_os:
                        print(args.host[0] + "'s Estimated Operation System : " + get_os(args.host[0]))
                    scans(port=args.ports, IP=str(args.host[0]))
                    for i in ports:
                        print(i)
                elif args.check_host and not args.ports and not args.port and not args.get_version and not args.Output and not args.fast_scan:
                    if args.get_os:
                        get_os(args.host[0])
                        is_up(args.host[0])
                    else:
                        is_up(args.host[0])
                elif args.fast_scan:
                    if args.verbose:
                        print("Fewer port selected, scanning 400 ports !")
                    if args.get_os:
                        get_os(args.host[0])
                        if args.check_host:
                            if not is_up(args.host[0]):
                                quit()
                            else:
                                scans(400, args.host[0])
                                for i in ports:
                                    print(i)
                        else:
                            scans(400, args.host[0])
                            for i in ports:
                                print(i)
                    else:
                        if args.check_host:
                            if not is_up(args.host[0]):
                                quit()
                            else:
                                scans(400, args.host[0])
                                for i in ports:
                                    print(i)
                        else:
                            scans(400, args.host[0])
                            for i in ports:
                                print(i)
                else:
                    if args.verbose:
                        print("No ports range was mentioned, trying first 1000 ports.")
                    if args.check_host:
                        if not is_up(args.host[0]):
                            quit()
                    if args.get_os:
                        print(args.host[0] + "'s Estimated Operation System : " + get_os(args.host[0]))
                    scans(port=1000, IP=str(args.host[0]))
                    for i in ports:
                        print(i)
            except ipaddress.AddressValueError:
                if "-" in args.host[0]:
                    ranges = args.host[0].split(".")[-1:].pop().split("-")
                    for address in range(int(ranges[0]), int(ranges[1]) + 1):
                        ip = args.host[0].split(".")[0] + "." + args.host[0].split(".")[1] + "." + args.host[0].split(".")[2] + "." + str(address)
                        if ipaddress.IPv4Address(ip):
                            if args.get_os:
                                print(ip + "'s Estimated Operation System : " + get_os(ip))
                            if args.check_host:
                                if not is_up(ip):
                                    continue
                            if args.port:
                                print(scan(port=args.port, IP=ip))
                            elif args.ports:
                                scans(port=args.ports, IP=ip)
                                for i in ports:
                                    print(i)
                            elif args.fast_scan:
                                scans(port=400, IP=ip)
                                for i in ports:
                                    print(i)
                        else:
                            raise ipaddress.AddressValueError
        elif "," in args.host:
            for ip in args.host:
                if "," in ip and len(ip) > 1:
                    ip = ip.split(',')[0]
                if args.check_host and ip != ",":
                    if not is_up(ip):
                        quit()
                if ip == ",":
                    continue
                elif ipaddress.IPv4Address(ip):
                    if args.get_os:
                        print(ip + "'s Estimated Operation System : " + get_os(ip))
                    if args.port:
                        print(scan(port=args.port, IP=ip))
                    elif args.ports:
                        scans(port=args.ports, IP=ip)
                        for i in ports:
                            print(i)
                    elif args.fast_scan:
                        scans(port=400, IP=ip)
                        for i in ports:
                            print(i)
                else:
                    raise ipaddress.AddressValueError
    # Keyboard interrupt !
    except KeyboardInterrupt:
        print("Take care !")
