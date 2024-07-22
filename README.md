# get_cert

Simple script to get the certificate info of a website.

Uses only the Python standard library. Caches results in `/tmp` for an hour.

## Minimum Requirements

* macOS or Linux
* [Python 3.11+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

## Recommended Requirements

* [asdf](https://asdf-vm.com/#/core-manage-asdf-vm)

## Installation

```bash
# clone the repository
git clone https://github.com/pythoninthegrass/get_cert.git
cd get_cert

# create a symbolic link to the script (recommended)
ln -s $(pwd)/get_cert.py ~/.local/bin/get-cert

# run standalone script (optional)
./get_cert.py
```

## Usage

```bash
# user input
λ get-cert 
Enter the FQDN of the server: [www.example.com]

google.com

Subject:              CN=*.google.com, O=N/A
Issuer:               CN=WR2, O=Google Trust Services
Valid from:           2024-06-24 06:35:44-05:00
Valid until:          2024-09-16 06:35:43-05:00

# positional argument
λ get-cert google.com

Subject:              CN=*.google.com, O=N/A
Issuer:               CN=WR2, O=Google Trust Services
Valid from:           2024-06-24 06:35:44-05:00
Valid until:          2024-09-16 06:35:43-05:00
```

## TODO

* Compile to a binary
  * cf. [PyInstaller](https://www.pyinstaller.org/) or [PyOxidizer](https://pyoxidizer.readthedocs.io/en/stable/)
