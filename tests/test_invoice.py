from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from lxml import etree

from invoice import NFSe, ServiceProvider, ServiceReceiver


class TestServiceProvider:
    def setup_method(self):
        invoice_path = Path(__file__).parent / "invoices.xml"
        self.xml_invoice = open(invoice_path, "r").read()

    def test_load_provider_from_xml_obj(self):
        root = etree.fromstring(self.xml_invoice).find(
            ".//{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}PrestadorServico"
        )
        provider = ServiceProvider._load(root)

        assert isinstance(provider, ServiceProvider)


class TestServiceReceiver:
    def setup_method(self):
        invoice_path = Path(__file__).parent / "invoices.xml"
        self.xml_invoice = open(invoice_path, "r").read()

    def test_load_receiver_from_xml_obj(self):
        root = etree.fromstring(self.xml_invoice).find(
            ".//{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}TomadorServico"
        )
        provider = ServiceReceiver._load(root)

        assert isinstance(provider, ServiceReceiver)



class TestInvoice:
    def setup_method(self):
        invoice_path = Path(__file__).parent / "invoices.xml"
        self.xml_invoice = open(invoice_path, "r").read()

    def test_load_invoice_from_string_xml(self):
        invoices = NFSe.load(self.xml_invoice)

        assert len(invoices) == 2

    def test_load_single_invoice_from_string_xml(self):
        root = etree.fromstring(self.xml_invoice).find(".//{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}Nfse")

        invoice = NFSe._load(root)

        assert isinstance(invoice, NFSe)
        assert invoice.numero == 59
        assert invoice.codigo_verificacao == "AAAA-BBBB"
        assert invoice.data_emissao == datetime(2022, 9, 5, 16, 37, 16)
        assert invoice.serie == 11
        assert invoice.tipo == 1
        assert invoice.data_emissao_rps == date(2022, 9, 5)
        assert invoice.natureza_operacao == 1
        assert invoice.optante_simples_nacional == 1
        assert invoice.incentivador_cultural == 2
        assert invoice.competencia == datetime(2022, 9, 5, 0, 0, 0)
        assert invoice.valor_servicos == Decimal(10600)
        assert invoice.iss_retido == 2
        assert invoice.base_calculo == Decimal(10600)
        assert invoice.valor_liquido == Decimal(10600)
        assert invoice.item_lista_servico == "0104"
        assert invoice.codigo_tributacao_municipio == "010401"
        assert invoice.discriminacao == "Descrição Serviço"
        assert invoice.codigo_municipio == 3304557
        assert isinstance(invoice.service_provider, ServiceProvider)
        assert isinstance(invoice.service_receiver, ServiceReceiver)

    def test_nfse_link(self):
        root = etree.fromstring(self.xml_invoice).find(".//{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}Nfse")

        invoice = NFSe._load(root)
        expected = "https://notacarioca.rio.gov.br/contribuinte/notaprint.aspx?inscricao=12345678&nf=59&verificacao=AAAABBBB"

        assert invoice.link == expected
