from __future__ import print_function
import socket
import socks
import smtplib
import datetime
import sys

# CRLF binary representationFor compatibility with Python 3.x
try:
    bCRLF = smtplib.bCRLF
except AttributeError:
    bCRLF = smtplib.CRLF


class NotSupportedProxyType(socks.ProxyError):
    """Not supported proxy type provided

    Exception is raised when provided proxy type is not supported.
    See socks.py for supported types.
    """


class SMTP(smtplib.SMTP):
    """This class manages a connection to an SMTP or ESMTP server.
    HTTP/SOCKS4/SOCKS5 proxy servers are supported

    For additional information see smtplib.py
    """

    def __init__(self, host='', port=0, proxy_host='', proxy_port=0, proxy_type=socks.HTTP,
                 local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        """Initialize a new instance.

        If a host is specified the connect method is called, and if it returns anything other than a
        success code an SMTPConnectError is raised

        :param host: Hostname of SMTP server
        :type host: string

        :param port: Port of SMTP server, by default smtplib.SMTP_PORT is used
        :type port: int

        :param proxy_host: Hostname of proxy server
        :type proxy_host: string

        :param proxy_port: Port of proxy server, by default port for specified  proxy type is used
        :type proxy_port: int

        :param proxy_type: Proxy type to use (see socks.PROXY_TYPES for details)
        :type proxy_type: int

        :param local_hostname: Local hostname is used as the FQDN of the local host for the
            HELO/EHLO command, if not specified the local hostname is found using socket.getfqdn()
        :type local_hostname: string

        :param timeout: Connection timeout
        :type timeout: int

        :param source_address: Host and port for the socket to bind to as its source address before
            connecting
        :type source_address: tuple
        """
        self._host = host
        self.timeout = timeout
        self.esmtp_features = {}
        self.command_encoding = 'ascii'
        self.source_address = source_address
        if host:
            if proxy_host:
                (code, msg) = self.connect_proxy(proxy_host, proxy_port, proxy_type, host, port)
            else:
                (code, msg) = self.connect(host, port)
            if code != 220:
                raise smtplib.SMTPConnectError(code, msg)
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            # RFC 2821 says we should use the fqdn in the EHLO/HELO verb, and
            # if that can't be calculated, that we should use a domain literal
            # instead (essentially an encoded IP address like [A.B.C.D]).
            fqdn = socket.getfqdn()
            if '.' in fqdn:
                self.local_hostname = fqdn
            else:
                # We can't find an fqdn hostname, so use a domain literal
                addr = '127.0.0.1'
                try:
                    addr = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    pass
                self.local_hostname = '[%s]' % addr

    def _print_debug(self, *args):
        """Method output debug message into stderr

        :param args: Message(s) to output
        :rtype args: string
        """
        if self.debuglevel > 1:
            print(datetime.datetime.now().time(), *args, file=sys.stderr)
        else:
            print(*args, file=sys.stderr)

    @classmethod
    def _parse_host(cls, host='localhost', port=0):
        """ Parse provided hostname and extract port number

        :param host: Server hostname
        :type host: string
        :param port: Server port
        :return: Tuple of (host, port)
        :rtype: tuple
        """
        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                host, port = host[:i], host[i + 1:]
                try:
                    port = int(port)
                except ValueError:
                    raise OSError('nonnumeric port')
        return host, port

    def _get_socket(self, host, port, timeout):
        # This makes it simpler for SMTP_SSL to use the SMTP connect code
        # and just alter the socket connection bit.
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socket.create_connection((host, port), timeout,
                                        self.source_address)

    def connect_proxy(self, proxy_host='localhost', proxy_port=0, proxy_type=socks.HTTP,
                      host='localhost', port=0):
        """Connect to a host on a given port via proxy server

        If the hostname ends with a colon (`:') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.

        Note: This method is automatically invoked by __init__, if a host and proxy server are
        specified during instantiation.

        :param proxy_host: Hostname of proxy server
        :type proxy_host: string

        :param proxy_port: Port of proxy server, by default port for specified  proxy type is used
        :type proxy_port: int

        :param proxy_type: Proxy type to use (see socks.PROXY_TYPES for details)
        :type proxy_type: int

        :param host: Hostname of SMTP server
        :type host: string

        :param port: Port of SMTP server, by default smtplib.SMTP_PORT is used
        :type port: int

        :return: Tuple of (code, msg)
        :rtype: tuple
        """
        if proxy_type not in socks.DEFAULT_PORTS.keys():
            raise NotSupportedProxyType
        (proxy_host, proxy_port) = self._parse_host(host=proxy_host, port=proxy_port)
        if not proxy_port:
            proxy_port = socks.DEFAULT_PORTS[proxy_type]
        (host, port) = self._parse_host(host=host, port=port)
        if self.debuglevel > 0:
            self._print_debug('connect: via proxy', proxy_host, proxy_port)
        s = socks.socksocket()
        s.set_proxy(proxy_type=proxy_type, addr=proxy_host, port=proxy_port)
        s.settimeout(self.timeout)
        if self.source_address is not None:
            s.bind(self.source_address)
        s.connect((host, port))
        # todo
        # Send CRLF in order to get first response from destination server.
        # Probably it's needed only for HTTP proxies. Further investigation required.
        s.sendall(bCRLF)
        self.sock = s
        (code, msg) = self.getreply()
        if self.debuglevel > 0:
            self._print_debug('connect:', repr(msg))
        return code, msg
