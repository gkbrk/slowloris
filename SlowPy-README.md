PySlow

PySlow is a Python implementation of the Slowloris DoS attack tool, originally created by Robert "RSnake" Hansen. It features a user-friendly graphical interface, which allows users to easily configure and launch Slowloris attacks against target websites.

This code is a fork of gkbrk/slowloris, which is a Python 2 implementation of Slowloris. The code has been updated to work with Python 3, and a GUI has been added by astrohippie.

-Requirements

To run PySlow, you need:

    Python 3.6 or higher
    PyQt5, a Python binding of the Qt GUI toolkit
    requests, a Python library for making HTTP requests

You can install PyQt5 and requests using pip, the Python package installer:

pip install PyQt5 requests

-Installation

To use PySlow, you can clone this GitHub repository and run the main.py file:

bash

git clone https://github.com/<your-username>/pyslow.git
cd pyslow
python main.py

Alternatively, you can download a ZIP archive of the code from the GitHub website, extract it to a directory of your choice, and run main.py from there.
Credits

PySlow is based on the Slowloris tool created by Robert "RSnake" Hansen. The original Slowloris code is available at:
    https://github.com/Ogglas/Orignal-Slowloris-HTTP-DoS (original source code)
    https://github.com/gkbrk/slowloris (forked source code)

The PySlow code has been forked from gkbrk/slowloris and modified by astrohippie, who added a GUI to the code. The modified code is available at:
    https://github.com/astrohippie/slowloris (modified)
