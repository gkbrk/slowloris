#!/usr/bin/python3
#=================================================================================================================================
#
#PySlow v1.0: "a Python GUI for slowloris stress testing" - (https://github.com/astrohippie/) - 2023 -> by AstroHippie
#-----------
#
#PySlow is based on the Slowloris tool created by Robert "RSnake" Hansen. -> https://twitter.com/rsnake
#Forked from: gkbrk on github -> https://github.com/gkbrk/slowloris
#Modified by: AstroHippie on github -> https://github.com/astrohippie
#
#----------- 
#
#PySlow is a Python-based tool for testing web servers against Slowloris attacks. Slowloris is a type of denial of service attack
#it aims to overwhelm a web server by opening and maintaining multiple connections to it, 
#thereby exhausting its resources and preventing legitimate traffic from being served.
# 
#=================================================================================================================================

#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import time
import tkinter as tk
from tkinter import messagebox

parser = argparse.ArgumentParser(
    description="PySlow, a Slowloris GUI written in Python, low bandwidth stress test tool for websites"
)

# Set up the GUI
root = tk.Tk()
root.title("PySlow Stress Test")
root.geometry("400x400")
root.resizable(False, False)

# Add labels and entry boxes for user input
host_label = tk.Label(root, text="Host:")
host_label.pack()
host_entry = tk.Entry(root, width=30)
host_entry.pack()

port_label = tk.Label(root, text="Port:")
port_label.pack()
port_entry = tk.Entry(root, width=30)
port_entry.pack()
port_entry.insert(0, "80")

sockets_label = tk.Label(root, text="Sockets:")
sockets_label.pack()
sockets_entry = tk.Entry(root, width=30)
sockets_entry.pack()
sockets_entry.insert(0, "150")

sleeptime_label = tk.Label(root, text="Sleep time (sec):")
sleeptime_label.pack()
sleeptime_entry = tk.Entry(root, width=30)
sleeptime_entry.pack()
sleeptime_entry.insert(0, "15")

proxy_var = tk.IntVar()
proxy_checkbox = tk.Checkbutton(root, text="Use Proxy", variable=proxy_var)
proxy_checkbox.pack()

proxy_host_label = tk.Label(root, text="Proxy Host:")
proxy_host_label.pack()
proxy_host_entry = tk.Entry(root, width=30)
proxy_host_entry.pack()
proxy_host_entry.insert(0, "127.0.0.1")

proxy_port_label = tk.Label(root, text="Proxy Port:")
proxy_port_label.pack()
proxy_port_entry = tk.Entry(root, width=30)
proxy_port_entry.pack()
proxy_port_entry.insert(0, "8080")

# Function to start the PySlow program with user input
def start_pyslow():
    # Get the user input from the GUI
    host = host_entry.get()
    port = port_entry.get()
    sockets = sockets_entry.get()
    sleeptime = sleeptime_entry.get()
    useproxy = proxy_var.get()
    proxy_host = proxy_host_entry.get()
    proxy_port = proxy_port_entry.get()

    # Set up the arguments for the PySlow program
    args = [
        sys.argv[0],
        host,
        "-p",
        port,
        "-s",
        sockets,
        "--sleeptime",
        sleeptime,
    ]
    if useproxy:
        args.extend(["-x", "--proxy-host", proxy_host, "--proxy-port", proxy_port])

    # Run the PySlow program with the specified arguments
    try:
        logging.info("Starting PySlow...")
        subprocess.run(args)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    else:
        logging.info("PySlow finished.")

# Add a button to start the PySlow program
start_button = tk.Button(root, text="Start", command=start_pyslow)
start_button.pack()

root.mainloop()
