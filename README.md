# get_cert

Simple script to get the certificate info of a website.

Uses only the Python standard library. Caches results in `/tmp` for an hour.

## Minimum Requirements

* macOS or Linux
* [Python 3.11+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

## Recommended Requirements

* [devbox](https://www.jetify.com/devbox/docs/installing_devbox/)
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

## Development

### Packaging

```bash
# activate dev environment
devbox shell

# compile to a binary
pyinstaller get_cert.spec --clean 

# deactivate dev environment
exit
```

## TODO

* Compile to a binary
  * Add [argv emulation](https://pyinstaller.org/en/stable/feature-notes.html?highlight=codesign-identity#optional-argv-emulation)
  * Debug error output
    ```bash
    Traceback (most recent call last):
    File "get_cert.py", line 123, in <module>
    File "get_cert.py", line 118, in main
    File "get_cert.py", line 65, in get_certificate
    File "ssl.py", line 517, in wrap_socket
    File "ssl.py", line 1104, in _create
    File "ssl.py", line 1382, in do_handshake
    ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)
    [26193] Failed to execute script 'get_cert' due to unhandled exception!
    ```
* [Sign the macOS binary](https://pyinstaller.org/en/stable/feature-notes.html?highlight=codesign-identity#macos-binary-code-signing)
  * Try [quill](https://github.com/anchore/quill)
* Reduce linux x86_64 binary size (~17MB vs. 7MB)
