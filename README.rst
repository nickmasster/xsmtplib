========
xsmtplib
========

THE PROJECT IS ARCHIVED. NO ISSUES / PULL REQUESTS CAN BE OPENED. FEEL FREE TO FORK.


An extension of standard smtplib, which supports proxy tunneling.

Package works on Python 2.7+ and Python 3.5+.

Using `PySocks <https://github.com/Anorov/PySocks>`_.

Installation
============
You can install **xsmtplib** from `PyPI <https://pypi.python.org/pypi>`_ by running::

    pip install xsmtplib

Or you can just download tarball / clone the repository and run::

    python setup.py install

Alternatively, include just *xsmtplib.py* in your project.

Usage
=====

**xsmtplib** extends standard python smtplib, so it can be used instead without any compatibility issues.

Connection to SMTP server via proxy can be done during instance initialization::

    from xsmtplib import SMTP

    server = SMTP(host="smtp.example.com", proxy_host="proxy.example.com")
    server.sendmail("user@example.com", "admin@example.com", "I have an issue. Please help!")
    server.quit()

Alternatively, you can connect to SMTP server manually when you need to::

    from xsmtplib import SMTP

    server = SMTP(timeout=30)
    server.set_debuglevel(1)
    server.connect_proxy(proxy_host="proxy.example.com", host="smtp.example.com")
    server.helo("user@example.com")
    server.sendmail("user@example.com", "admin@example.com", "I have an issue. Please help!")
    s.quit()

Known issues
============
SMTPS (SSL SMTP) and LMTP connections via proxy are not supported yet.

License
=======

See `<LICENSE>`_ file for more details.
