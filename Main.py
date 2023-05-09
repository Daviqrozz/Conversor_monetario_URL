import requests
import json
import re

class ExtratorURL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self, url):
        if type(url) == str:
            return url.strip()
        else:
            return ""

    def valida_url(self):
        if not self.url:
            raise ValueError("A URL está vazia")

        padrao_url = re.compile('(http(s)?://)?(www.)?bytebank.com(.br)?/cambio')
        match = padrao_url.match(url)
        if not match:
            raise ValueError("A URL não é válida.")

    def get_url_base(self):
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self):
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao + 1:]
        return url_parametros

    def get_valor_parametro(self, parametro_busca):
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        indice_valor = indice_parametro + len(parametro_busca) + 1
        indice_e_comercial = self.get_url_parametros().find('&', indice_valor)
        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]
        return valor

    def get_cotacao(self,moeda):
        cotacoes = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL')
        cotacoes = cotacoes.json()
        if moeda == 'DOLAR':
            valorDolar = cotacoes['USDBRL']['bid']
            valor = valorDolar
            return float(valor)
        elif moeda == 'EURO':
            valorEuro = cotacoes['EURBRL']['bid']
            valor = valorEuro
            return float(valor)

#Inputs

origem = str(input('Qual moeda sera convertida -> (Dolar/Real/Euro):')).upper()
quantidade = int(input('Digite a quantia a ser convertida: '))
destino = str(input('A moeda sera convertida em Dolar,Real ou Euro?:')).upper()

#Variaveis
url = f"bytebank.com/cambio?quantidade={quantidade}&moedaOrigem={origem}&moedaDestino={destino}"
extrator_url = ExtratorURL(url)
valor_quantidade = extrator_url.get_valor_parametro('quantidade')
moedaorigem = extrator_url.get_valor_parametro('moedaOrigem')
moedadestino = extrator_url.get_valor_parametro('moedaDestino')


# Cotaçoes
cotaçaoDolar = extrator_url.get_cotacao('DOLAR')
cotaçaoEuro = extrator_url.get_cotacao('EURO')


#DOLAR/REAL
if moedaorigem == 'DOLAR' and moedadestino == 'REAL':
    valor_final = float(valor_quantidade) * cotaçaoDolar
    print(f'{valor_quantidade}$ equivalem a {valor_final:.1f}R$')
elif moedaorigem == 'REAL' and moedadestino == 'DOLAR':
    valor_final = float(valor_quantidade) / cotaçaoDolar
    print(f'{valor_quantidade}R$ equivalem a {valor_final:.1f}$')

#EURO/REAL
elif moedaorigem == 'EURO' and moedadestino == 'REAL':
    valor_final = float(valor_quantidade) / cotaçaoEuro
    print(f'{valor_quantidade}€ equivalem a {valor_final:.1f}R$')
elif moedaorigem == 'REAL' and moedadestino == 'EURO':
    valor_final = float(valor_quantidade) * cotaçaoEuro
    print(f'{valor_quantidade}R$ equivalem a {valor_final:.1f}€')

#DOLAR/EURO
elif moedaorigem == 'DOLAR' and moedadestino == 'EURO':
    valor_final = float(valor_quantidade) / cotaçaoDolar - cotaçaoEuro
    print(f'Conversao entre {moedadestino} e {moedaorigem} ainda nao esta disponivel')
elif moedaorigem == 'EURO' and moedadestino == 'DOLAR':
    valor_final = float(valor_quantidade) * cotaçaoEuro - cotaçaoDolar
    print(f'Conversao entre {moedaorigem} e {moedadestino} ainda nao esta disponivel')
else:
    print(f'Nao é possivel fazer a converão entre {moedaorigem} e {moedadestino}')













