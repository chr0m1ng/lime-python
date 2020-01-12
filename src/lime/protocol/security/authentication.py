from enum import Enum


class AuthenticationScheme(Enum):

    GUEST = 'guest'
    PLAIN = 'plain'
    TRANSPORT = 'transport'
    KEY = 'key'
    EXTERNAL = 'external'


class Authentication:

    # scheme property
    @property
    def scheme(self):
        return self.__scheme

    @scheme.setter
    def scheme(self, value):
        if isinstance(value, AuthenticationScheme):
            self.__scheme = value
        else:
            raise ValueError('scheme must be a AuthenticationScheme')


class GuestAuthentication(Authentication):

    def __init__(self):
        self.scheme = AuthenticationScheme.GUEST


class TransportAuthentication(Authentication):

    def __init__(self):
        self.scheme = AuthenticationScheme.TRANSPORT


class PlainAuthentication(Authentication):

    # password property
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self.__password = value
        else:
            raise ValueError('password must be a str')

    def __init__(self, password):
        self.scheme = AuthenticationScheme.PLAIN
        self.password = password


class KeyAuthentication(Authentication):

    # key property
    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        if isinstance(value, str):
            self.__key = value
        else:
            raise ValueError('key must be a str')

    def __init__(self, key):
        self.scheme = AuthenticationScheme.KEY
        self.key = key


class ExternalAuthentication(Authentication):

    # token property
    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        if isinstance(value, str):
            self.__token = value
        else:
            raise ValueError('token must be a str')

    # issuer property
    @property
    def issuer(self):
        return self.__issuer

    @issuer.setter
    def issuer(self, value):
        if isinstance(value, str):
            self.__issuer = value
        else:
            raise ValueError('issuer must be a str')

    def __init__(self, token, issuer):
        self.scheme = AuthenticationScheme.EXTERNAL
        self.token = token
        self.issuer = issuer
