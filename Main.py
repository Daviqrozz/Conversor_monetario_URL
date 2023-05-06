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

    def __len__(self):
        return len(self.url)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url

origem = str(input('Qual moeda sera convertida -> (Dolar/Real):')).upper()
quantidade = int(input('Digite a quantia a ser convertida: '))
destino = str(input('A moeda sera convertida em Dolar ou Real:')).upper()

url = f"bytebank.com/cambio?quantidade={quantidade}&moedaOrigem={origem}&moedaDestino={destino}"
extrator_url = ExtratorURL(url)
valor_quantidade = extrator_url.get_valor_parametro('quantidade')
moedaorigem = extrator_url.get_valor_parametro('moedaOrigem')
moedadestino = extrator_url.get_valor_parametro('moedaDestino')

print(extrator_url)
# Conversão de dólar para real
cotaçaoDolar = 5.50
if moedaorigem == 'DOLAR' and moedadestino == 'REAL':
    valor = int(valor_quantidade) * cotaçaoDolar
    print(f'{valor_quantidade}$ equivalem a {valor}R$')
elif moedaorigem == 'REAL' and moedadestino == 'DOLAR':
    valor = float(valor_quantidade) / cotaçaoDolar
    print(f'{valor_quantidade}R$ equivalem a {valor:.1f}$')
else:
    print(f'Nao é possivel converter de {moedaorigem} para {moedadestino}')






