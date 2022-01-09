# Port Scanner
 Run this script in order to scan ports of hosts inside your network !<br/>
 In case of troubles type --help or -h to get the help menu.
 
 # Examples
 python Mapper.py 10.10.11.103 --ports 1200 -Gv --Output scan.txt <br/>
 python Mapper.py 10.10.11.1-100 -P 100 -O scan.txt<br/>
 python Mapper.py 10.10.11.13 , 10.10.11.15 , 10.10.11.19 --port 22 --Output scan.txt

# Usage
--port, -p : select a single port to check, Example : python3 Mapper.py 10.10.11.13 --port 80 <br/>
--ports, -P : select a port range to check, Example : python3 Mapper.py 10.10.11.13 --ports 100 <br/>
--verbose, -v : Prints the process verbosity, Example : python3 Mapper.py 10.10.11.13 -P 100 -v <br/>
--Output, -O : Prints the output into a file, Example : python3 Mapper.py 10.10.11.13 --ports 100 --Output 100_ports.txt <br/>
--get_version, -Gv : Prints estimated services version, Example : python3 Mapper.py 10.10.11.13 --port 22 -Gv
