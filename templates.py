gerar = '''
<EnviarLoteRpsEnvio>
    <LoteRps Id="TesteDeLote">
        <NumeroLote>{{nfse.numero_lote}}</NumeroLote>
        <Cnpj>{{nfse.cnpj}}</Cnpj>
        <InscricaoMunicipal>{{nfse.inscricao_municipal}}</InscricaoMunicipal>
        <QuantidadeRps>1</QuantidadeRps>
        <ListaRps>
            <Rps>
                <InfRps Id="idRPS">
                    <IdentificacaoRps>
                        <Numero>{{nfse.numero}}</Numero>
                        <Serie>{{nfse.serie}}</Serie>
                        <Tipo>{{nfse.tipo}}</Tipo>
                    </IdentificacaoRps>
                    <DataEmissao>{{nfse.data_emissao}}</DataEmissao>
                    <NaturezaOperacao>{{nfse.natureza_operacao}}</NaturezaOperacao>
                    <OptanteSimplesNacional>{{nfse.optante_simples_nacional}}</OptanteSimplesNacional>
                    <IncentivadorCultural>{{nfse.incentivador_cultural}}</IncentivadorCultural>
                    <Status>{{nfse.status}}</Status>
                    <Servico>
                        <Valores>
                            <ValorServicos>{{nfse.valor_servicos}}</ValorServicos>
                            <ValorDeducoes>{{nfse.valor_deducoes}}</ValorDeducoes>
                            <ValorPis>{{nfse.valor_pis}}</ValorPis>
                            <ValorCofins>{{nfse.valor_cofins}}</ValorCofins>
                            <ValorInss>{{nfse.valor_inss}}</ValorInss>
                            <ValorIr>{{nfse.valor_ir}}</ValorIr>
                            <ValorCsll>{{nfse.valor_csll}}</ValorCsll>
                            <IssRetido>{{nfse.iss_retido}}</IssRetido>
                            <ValorIss>{{nfse.valor_iss}}</ValorIss>
                            <OutrasRetencoes>{{nfse.outras_retencoes}}</OutrasRetencoes>
                            <Aliquota>{{nfse.aliquota}}</Aliquota>
                            <DescontoIncondicionado>{{nfse.desconto_incondicionado}}</DescontoIncondicionado>
                            <DescontoCondicionado>{{nfse.desconto_condicionado}}</DescontoCondicionado>
                        </Valores>
                        <ItemListaServico>{{nfse.item_lista_servico}}</ItemListaServico>
                        <CodigoTributacaoMunicipio>{{nfse.codigo_tributacao_municipio}}</CodigoTributacaoMunicipio>
                        <Discriminacao>{{nfse.discriminacao}}</Discriminacao>
                        <CodigoMunicipio>{{nfse.discriminacao}}</CodigoMunicipio>
                    </Servico>
                    <Prestador>
                        <Cnpj>{{nfse.service_provider.cnpj}}</Cnpj>
                        <InscricaoMunicipal>{{nfse.service_provider.inscricao_municipal}}</InscricaoMunicipal>
                    </Prestador>
                    <Tomador>
                        <IdentificacaoTomador>
                            <CpfCnpj>
                                {% if nfse.pessoa_juridica %}
                                    <Cnpj>{{nfse.service_receiver.cpf_cnpj}}</Cnpj>
                                {% else %}
                                    <Cpf>{{nfse.service_receiver.cpf_cnpj}}</Cpf>
                                {% end %}
                            </CpfCnpj>
                        </IdentificacaoTomador>
                        <RazaoSocial>{{nfse.service_receiver.razao_social}}</RazaoSocial>
                        <Endereco>
                            <Endereco>{{nfse.service_receiver.endereco}}</Endereco>
                            <Numero>{{nfse.service_receiver.numero}}</Numero>
                            <Complemento>{{nfse.service_receiver.complemento}}</Complemento>
                            <Bairro>{{nfse.service_receiver.bairro}}</Bairro>
                            <CodigoMunicipio>{{nfse.service_receiver.codigo_municipio}}</CodigoMunicipio>
                            <Uf>{{nfse.service_receiver.uf}}</Uf>
                            <Cep>{{nfse.service_receiver.cep}}</Cep>
                        </Endereco>
                        <Contato>
                            <Email>{{nfse.service_receiver.email}}</Email>
                        </Contato>
                    </Tomador>
                </InfRps>
            </Rps>
        </ListaRps>
    </LoteRps>
</EnviarLoteRpsEnvio>
'''


consultar = '''<?xml version="1.0" encoding="iso-8859-1"?>
<ConsultarNfseEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
<Prestador>
   <Cnpj>{{cnpj}}</Cnpj>
   <InscricaoMunicipal>{{inscricao_municipal}}</InscricaoMunicipal>  
</Prestador>
<PeriodoEmissao>
   <DataInicial>{{data_inicial}}</DataInicial> 
   <DataFinal>{{data_final}}</DataFinal> 
</PeriodoEmissao>
</ConsultarNfseEnvio> 
'''
