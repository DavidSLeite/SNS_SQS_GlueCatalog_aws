import json

def _leituraArquivo() -> str:
    """ Função que faz leitura do conteudo do arquivo """
    try:
        print('Inicianco Leitura do Arquivo JSON')
        with open('jsonArquivo.json') as arquivo:
            conteudo = arquivo.read()
    except:
        raise Exception('Erro ao lêr o arquivo, inexistente ou com nome diferente de "jsonEntrada.json" ')    

    return conteudo

def _convertConteudoToJson() -> json:
    """ Função converte texto e valida se o conteudo é um JSON válido """
    conteudo = _leituraArquivo()
    try:
        conteudoJson = json.loads(conteudo)
    except:
        raise Exception('Erro, arquivo encontrado porém conteudo JSON está inválido') 

    #função que trata conteudoJson
    def _validaConteudoJson(a):
        for key ,values in a.items():

            lista_tipo_valido = ['string', 'integer', 'boolean', 'date', 'timestamp', 'double']

            # verifica se valor do atributo é uma tipo válido conforme lista
            if not values in lista_tipo_valido and str(type(values)) == "<class 'str'>":
                raise Exception(f'erro em "{key}":"{values}", atributo "{values}" inválido!')

            # verificação de forma recursiva no dict
            if str(type(values)) == "<class 'dict'>":
                _validaConteudoJson(values)

            # a lista só pode haver um elemento senão gerar erro!!!
            if str(type(values)) == "<class 'list'>":
                if len(values) > 1:
                    raise Exception(f'erro em lista "{key}":"{values}", lista contém mais de um elemento !')
            
            # verifica e valida valor dentro da lista
            if str(type(values)) == "<class 'list'>":
                # verifica se valor dentro da lista é um atributoo válido
                if not values[0] in lista_tipo_valido and str(type(values[0])) == "<class 'str'>":
                    raise Exception(f'erro em "{key}":"{values[0]}", atributo "{values[0]}" inválido!')

                # verificação de forma recursiva no dict
                if str(type(values[0])) == "<class 'dict'>":
                    _validaConteudoJson(values[0])

    _validaConteudoJson(conteudoJson)

    return conteudoJson

def _geraArquivoJoson():
    """ Função gera arquivo tratado """
    with open('saidaJSON.json', 'w')  as saida:
        a = _convertConteudoToJson()
        saida.write(json.dumps(a, indent = 4))
    print('Arquivo gerado com sucesso!!!')


if __name__ == '__main__':
    _geraArquivoJoson()
