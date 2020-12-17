# importação de bibliotecas utilizadas
import requests
import json
import re
from bs4 import BeautifulSoup

qtdRow = 110 # nr maximo de rows por requisicao
ufList = ['RS','SC'] # UFs que serao buscadas
data = {} # inicializacao da variavel que guardará o resultado final

# funcao que faz um POST na URL dos correios e retorna o HTML como resultado
def reqFaixaCep(uf, pagini, pagfim):
  payload = {'UF': uf, 'qtdrow': qtdRow, 'pagini': pagini, 'pagfim': pagfim}
  try:
    r = requests.post('http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm', data=payload)
  except requests.exceptions.RequestException as e:
    print('An error has occurred. Please try again later.')
    raise SystemExit(e)

  return r

# funcao que retorna o numero maximo de registros do UF em questao
def findMaxRow(uf, startRow, endRow):
  page = reqFaixaCep(uf, startRow, endRow)
  soup = BeautifulSoup(page.text, 'html.parser')
  findMaxRow = soup.find(text=re.compile('1 a 110 de '))
  if (findMaxRow):
    words = findMaxRow.strip().split()
    return words[-1]
  else:
    return 0

# funcao que busca no HTML todas as informacoes referentes ao CEP disponibilizadas na pagina
# e adiciona em uma lista dicionarios com pares de chave valor
def getCepList(page):
  global id
  soup = BeautifulSoup(page.text, 'html.parser')
  content = soup.find('div', class_='ctrlcontent')

  tableRows = content.find_all('tr')

  for tableRow in tableRows:
    cells = tableRow.findAll('td')
    info = {}
    info['id'] = id

    aux = 0
    for cell in cells:
      if (aux == 0):
        info['Localidade'] = cell.text
      elif (aux == 1):
        info['Faixa de CEP'] = cell.text
      elif (aux == 2):
        info['Situação'] = cell.text
      elif (aux == 3):
        info['Tipo de faixa'] = cell.text
      else:
        info[aux] = cell.text
      aux += 1
    
    if (len(info) > 3):
      cepList.append(info)
      id += 1
    else:
      pass

# loop que passa por todos os index (UFs) na variavel ufList
for uf in ufList:
  id = 0
  startRow = 1
  endRow = 110
  maxRow = int(findMaxRow(uf, startRow, endRow))
  cepList = []
  page = reqFaixaCep(uf, startRow, endRow)

  getCepList(page)

  # loop para buscar todas as paginas
  while endRow <= maxRow:
    startRow = endRow + 1
    endRow += qtdRow
    page = reqFaixaCep(uf, startRow, endRow)

    getCepList(page)

  # adiciona a lista completa das faixas de cep no dicionario data de acordo com a UF selecionada
  data.update({uf: cepList})

# exporta as faixas de cep encontradas em cada UF para um arquivo .json
with open('faixas_de_cep.json', 'w', encoding='utf8') as fp:
  json.dump(data, fp, ensure_ascii=False)
  
# print(data)


