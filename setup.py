from setuptools import setup, find_packages

setup(
    name="DorkXploit",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "colorama",
        "logging",
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "dorkxploit=main:main",
        ],
    },
)
