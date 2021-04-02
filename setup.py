from distutils.core import setup

setup(
    name="Slowloris",
    py_modules=["slowloris"],
    entry_points={"console_scripts": ["slowloris=slowloris:main"]},
    version="0.2.3",
    description="Low bandwidth DoS tool. Slowloris rewrite in Python.",
    author="Gokberk Yaltirakli",
    author_email="opensource@gkbrk.com",
    url="https://github.com/gkbrk/slowloris",
    keywords=["dos", "http", "slowloris"],
    license="MIT",
)
