from pathlib import Path
from unittest import mock
from uuid import uuid4

from certificate import Certificate


class TestCertificate:
    path = "/path/to/certicate.pfx"
    password = "password"

    @mock.patch.object(Certificate, "_open", return_value=(b"cert", b"key"))
    @mock.patch("certificate.NamedTemporaryFile")
    def test_cert(self, m_file, m_open):
        temp_file_name = f"/tmp/{str(uuid4())[:5]}_cert.pem"
        m_temp_file = mock.Mock()
        m_temp_file.name = temp_file_name
        m_file.return_value = m_temp_file

        c = Certificate(self.path, self.password)
        cert = c.cert

        assert cert == Path(temp_file_name)
        assert cert.read_bytes() == b"cert"
        m_file.assert_called_once_with(suffix=".pem", delete=False)

        c.cert.unlink()

    @mock.patch.object(Certificate, "_open", return_value=(b"cert", b"key"))
    @mock.patch("certificate.NamedTemporaryFile")
    def test_key(self, m_file, m_open):
        temp_file_name = f"/tmp/{str(uuid4())[:5]}_key.pem"
        m_temp_file = mock.Mock()
        m_temp_file.name = temp_file_name
        m_file.return_value = m_temp_file

        c = Certificate(self.path, self.password)
        key = c.key

        assert key == Path(temp_file_name)
        assert key.read_bytes() == b"key"
        m_file.assert_called_once_with(suffix=".pem", delete=False)

        c.key.unlink()

    @mock.patch.object(Certificate, "_Certificate__cert_path")
    @mock.patch.object(Certificate, "_open", return_value=(b"cert", b"key"))
    @mock.patch("certificate.NamedTemporaryFile")
    def test_cert_do_not_reopen_if_file_still_exists(self, m_file, m_open, m_cert_path):
        m_cert_path.exists.return_value = True
        c = Certificate(self.path, self.password)

        assert c.cert == m_cert_path

        m_file.assert_not_called()

    @mock.patch.object(Certificate, "_Certificate__key_path")
    @mock.patch.object(Certificate, "_open", return_value=(b"cert", b"key"))
    @mock.patch("certificate.NamedTemporaryFile")
    def test_key_do_not_reopen_if_file_still_exists(self, m_file, m_open, m_key_path):
        m_key_path.exists.return_value = True
        c = Certificate(self.path, self.password)

        assert c.key == m_key_path

        m_file.assert_not_called()
