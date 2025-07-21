# python3-cyberfusion-proftpd-support

Library to manage ProFTPD.

At the moment, this library allows you to create auto-expiring ProFTPD users (stored in an SQLite database).

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-proftpd-support

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

Place settings in `/etc/proftpd-support.conf` (regular text file).

All settings must be prefixed with `PROFTPD_SUPPORT_`.

Find all available settings in `settings.py`.

Find an example config in `.env.local`.

# Usage

```python
from cyberfusion.ProftpdSupport.users import create_proftpd_user

user = create_proftpd_user(
    username="example",
    password="example",
    uid=1000,
    gid=1000,
    home_directory="/home/example",
)
```
