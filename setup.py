from setuptools import setup, find_packages

def read_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name="ipn",
    version="0.5",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "tabulate",
        "toml",
        "colorama",
        "requests",
        "packaging",
    ],
    entry_points={
        "console_scripts": [
            "ipn=ipn.main:main",
        ],
    },
    author="Errik Rose",
    author_email="errik.rose@kitsunedb.com",
    description="A simple tool to display network information",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/marokarr/ipn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
