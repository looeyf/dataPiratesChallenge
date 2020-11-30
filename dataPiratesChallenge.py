import requests
import json
import re
from bs4 import BeautifulSoup

qtdRow = 110 # nr maximo de rows por requisicao
ufList = ['RS','SC'] # UFs que serao buscadas
data = {} # resultado final

def reqFaixaCep(uf, pagini, pagfim):
  payload = {'UF': uf, 'qtdrow': qtdRow, 'pagini': pagini, 'pagfim': pagfim}
  try:
    r = requests.post('http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm', data=payload, allow_redirects=False)
  except requests.exceptions.RequestException as e:
    print('An error has occurred. Please try again later.')
    raise SystemExit(e)

  return r

def findMaxRow(uf, startRow, endRow):
  page = reqFaixaCep(uf, startRow, endRow)
  soup = BeautifulSoup(page.text, 'html.parser')
  findMaxRow = soup.find(text=re.compile('1 a 110 de '))
  if (findMaxRow):
    words = findMaxRow.strip().split()
    return words[-1]
  else:
    return 0

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

for uf in ufList:
  id = 0
  startRow = 1
  endRow = 110
  maxRow = int(findMaxRow(uf, startRow, endRow))
  cepList = []
  page = reqFaixaCep(uf, startRow, endRow)

  # logica para inserir os valores em uma list abaixo e pegar o maxrow do html
  getCepList(page)

  while endRow <= maxRow:
    startRow = endRow + 1
    endRow += qtdRow
    page = reqFaixaCep(uf, startRow, endRow)

    # logica para inserir os valores em uma list abaixo
    getCepList(page)

  data.update({uf: cepList})

with open('faixas_de_cep.json', 'w') as fp:
  json.dump(data, fp)
# print(data)


