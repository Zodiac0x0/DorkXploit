from setuptools import setup, find_packages

setup(
    name="DorkXploit",
    version="1.0",
    description= "Automated tool For Dorking",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "colorama",
        "logging",
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security'],
    entry_points={
        "console_scripts": [
            "dorkxploit=main:main",
        ],
    },
)
