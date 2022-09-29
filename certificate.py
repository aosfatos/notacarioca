from pathlib import Path
from tempfile import NamedTemporaryFile

from OpenSSL import crypto


class Certificate:
    __cert_path = None
    __key_path = None

    def __init__(self, path: Path, password: str):
        self.path = path
        self.password = password
        self.__cert, self.__key = self._open()

    @property
    def cert(self):
        if self.__cert_path is None or not self.__cert_path.exists():
            temp = NamedTemporaryFile(suffix=".pem", delete=False)
            with open(temp.name, "wb") as fobj:
                fobj.write(self.__cert)
            self.__cert_path = Path(temp.name)

        return self.__cert_path

    @property
    def key(self):
        if self.__key_path is None or not self.__key_path.exists():
            temp = NamedTemporaryFile(suffix=".pem", delete=False)
            with open(temp.name, "wb") as fobj:
                fobj.write(self.__key)
            self.__key_path = Path(temp.name)

        return self.__key_path

    def _open(self):
        with open(self.path, "rb") as fid:
            pfx = crypto.load_pkcs12(fid.read(), self.password)

        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
        return cert, key
