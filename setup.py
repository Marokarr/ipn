from setuptools import setup, find_packages

setup(
    name="ipn",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "tabulate",
        "toml",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "ipn=ipn.ipn:main",
        ],
    },
    author="Errik Rose",
    author_email="errik.rose@kitsunedb.com",
    description="A simple tool to display network information",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marokarr/ipn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
