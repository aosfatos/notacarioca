from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from lxml import etree


class Invoice:
    xml_ns = "{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}"

    @classmethod
    def _get(cls, ele, field):
        return getattr(ele.find(f".//{cls.xml_ns}{field}"), "text", None)

    @classmethod
    def _get_all(cls, ele, field, pos=0):
        value = None
        if attributes := ele.findall(f".//{cls.xml_ns}{field}"):
            value = attributes[pos].text

        return value

    @classmethod
    def load(cls):
        raise NotImplementedError


@dataclass
class ServiceReceiver(Invoice):
    cnpj: str
    inscricao_municipal: str
    razao_social: str
    endereco: str
    numero: str
    complemento: str
    bairro: str
    codigo_municipio: int
    uf: str
    cep: str
    telefone: str
    email: str


    @classmethod
    def _load(cls, xml_obj):
        return cls(
            cnpj=cls._get(xml_obj, "Cnpj"),
            inscricao_municipal=cls._get(xml_obj, "InscricaoMunicipal"),
            razao_social=cls._get(xml_obj, "RazaoSocial"),
            endereco=cls._get_all(xml_obj, "Endereco", pos=1),
            numero=cls._get(xml_obj, "Numero"),
            complemento=cls._get(xml_obj, "Complemento"),
            bairro=cls._get(xml_obj, "Bairro"),
            codigo_municipio=cls._get(xml_obj, "CodigoMunicipio"),
            uf=cls._get(xml_obj, "Uf"),
            cep=cls._get(xml_obj, "Cep"),
            telefone=cls._get(xml_obj, "Telefone"),
            email=cls._get(xml_obj, "Email"),
        )


@dataclass
class ServiceProvider(Invoice):
    cnpj: str
    inscricao_municipal: str
    razao_social: str
    nome_fantasia: str
    endereco: str
    numero: str
    complemento: str
    bairro: str
    codigo_municipio: int
    uf: str
    cep: str
    telefone: str
    email: str


    @classmethod
    def _load(cls, xml_obj):
        return cls(
            cnpj=cls._get(xml_obj, "Cnpj"),
            inscricao_municipal=cls._get(xml_obj, "InscricaoMunicipal"),
            razao_social=cls._get(xml_obj, "RazaoSocial"),
            nome_fantasia=cls._get(xml_obj, "NomeFantasia"),
            endereco=cls._get_all(xml_obj, "Endereco", pos=1),
            numero=cls._get(xml_obj, "Numero"),
            complemento=cls._get(xml_obj, "Complemento"),
            bairro=cls._get(xml_obj, "Bairro"),
            codigo_municipio=cls._get(xml_obj, "CodigoMunicipio"),
            uf=cls._get(xml_obj, "Uf"),
            cep=cls._get(xml_obj, "Cep"),
            telefone=cls._get(xml_obj, "Telefone"),
            email=cls._get(xml_obj, "Email"),
        )


@dataclass
class NFSe(Invoice):
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
    service_provider: ServiceProvider
    service_receiver: ServiceReceiver

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
    def _load(cls, nfse):
        service_provider = ServiceProvider._load(nfse.find(f".//{cls.xml_ns}PrestadorServico"))
        service_receiver = ServiceReceiver._load(nfse.find(f".//{cls.xml_ns}TomadorServico"))
        return cls(
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
            service_provider=service_provider,
            service_receiver=service_receiver,
        )

    @classmethod
    def load(cls, content):
        root = etree.fromstring(content)
        invoices = []
        nfses = root.findall(f".//{cls.xml_ns}Nfse")

        for nfse in nfses:
            invoices.append(cls._load(nfse))

        return invoices
