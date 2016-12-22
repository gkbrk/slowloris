from distutils.core import setup
setup(
    name = "Slowloris",
    py_modules = ["slowloris"],
    entry_points = {"console_scripts": ["slowloris=slowloris:main"]},
    version = "0.1.4",
    description = "Low bandwidth DoS tool. Slowloris rewrite in Python.",
    author = "Gokberk Yaltirakli",
    author_email = "webdosusb@gmail.com",
    url = "https://github.com/gkbrk/slowloris",
    keywords = ["dos", "http", "slowloris"]
)
