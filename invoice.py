from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from lxml import etree


@dataclass
class NFSe:
    xml_ns = "{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}"

    numero: int
    codigo_verificacao: str
    data_emissao: datetime
    serie: int
    tipo: int
    data_emissao_rps: date
    natureza_operacao: int
    optante_simples_nacional: int
    incentivador_cultural: int
    competencia: datetime
    valor_servicos: Decimal
    iss_retido: int
    base_calculo: Decimal
    valor_liquido: Decimal
    item_lista_servico: str
    codigo_tributacao_municipio: str
    discriminacao: str
    codigo_municipio: int

    def __post_init__(self):
        self.numero = int(self.numero)
        self.data_emissao = datetime.strptime(self.data_emissao, "%Y-%m-%dT%H:%M:%S")
        self.serie = int(self.serie)
        self.tipo = int(self.tipo)
        self.data_emissao_rps = datetime.strptime(self.data_emissao_rps, "%Y-%m-%d").date()
        self.natureza_operacao = int(self.natureza_operacao)
        self.optante_simples_nacional = int(self.optante_simples_nacional)
        self.incentivador_cultural = int(self.incentivador_cultural)
        self.competencia = datetime.strptime(self.competencia, "%Y-%m-%dT%H:%M:%S")
        self.valor_servicos = Decimal(self.valor_servicos)
        self.iss_retido = int(self.iss_retido)
        self.base_calculo = Decimal(self.base_calculo)
        self.valor_liquido = Decimal(self.valor_liquido)
        self.codigo_municipio = int(self.codigo_municipio)

    @classmethod
    def _get(cls, ele, field):
        return getattr(ele.find(f".//{cls.xml_ns}{field}"), "text", None)

    @classmethod
    def _load(cls, nfse):
        return NFSe(
            numero = cls._get(nfse, "Numero"),
            codigo_verificacao=cls._get(nfse, "CodigoVerificacao"),
            data_emissao=cls._get(nfse, "DataEmissao"),
            serie=cls._get(nfse, "Serie"),
            tipo=cls._get(nfse, "Tipo"),
            data_emissao_rps=cls._get(nfse, "DataEmissaoRps"),
            natureza_operacao=cls._get(nfse, "NaturezaOperacao"),
            optante_simples_nacional=cls._get(nfse, "OptanteSimplesNacional"),
            incentivador_cultural=cls._get(nfse, "IncentivadorCultural"),
            competencia=cls._get(nfse, "Competencia"),
            valor_servicos=cls._get(nfse, "ValorServicos"),
            iss_retido=cls._get(nfse, "IssRetido"),
            base_calculo=cls._get(nfse, "BaseCalculo"),
            valor_liquido=cls._get(nfse, "ValorLiquidoNfse"),
            item_lista_servico=cls._get(nfse, "ItemListaServico"),
            codigo_tributacao_municipio=cls._get(nfse, "CodigoTributacaoMunicipio"),
            discriminacao=cls._get(nfse, "Discriminacao"),
            codigo_municipio=cls._get(nfse, "CodigoMunicipio"),
        )

    @classmethod
    def load(cls, content):
        root = etree.fromstring(content)
        invoices = []
        nfses = root.findall(f".//{cls.xml_ns}Nfse")

        for nfse in nfses:
            invoices.append(cls._load(nfse))

        return invoices
