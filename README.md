#slowloris.py - Simple slowloris in Python#

##What is Slowloris?##
Slowloris is basically an HTTP Denial of Service attack that affects threaded servers. It works like this:

1. We start making lots of HTTP requests.
2. We send headers periodically (every ~15 seconds) to keep the connections open.
3. We never close the connection unless the server does so. If the server closes a connection, we create a new one keep doing the same thing.

This exhausts the servers thread pool and the server can't reply to other people.

##How to install and run?##

You can clone the git repo or install using **pip**. Here's how you run it.

* `sudo pip3 install slowloris`
* `slowloris example.com`

That's all it takes to install and run slowloris.py.

If you want to clone using git instead of pip, here's how you do it.

* `git clone https://github.com/gkbrk/slowloris.git`
* `cd slowloris`
* `python3 slowloris.py example.com`

##License##

The code is licensed under the MIT License.
