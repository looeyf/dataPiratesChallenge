import requests
import re
from bs4 import BeautifulSoup

qtdRow = 112 # nr maximo de rows por requisicao
ufList = ['RS'] # UFs que serao buscadas
data = {} # resultado final

# data = {
#     'RS': [
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'}
#     ],
#     'SC': [
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'},
#       {'id':0, 'faixaCep':'tal a tal', 'localidade':'passo fundo'}
#     ]
# }
# 

def reqFaixaCep(uf, pagini, pagfim):
  payload = {'UF': uf, 'Localidade':'Passo Fundo','qtdrow': qtdRow, 'pagini': pagini, 'pagfim': pagfim}
  # payload = {'UF': uf, 'qtdrow': qtdRow, 'pagini': pagini, 'pagfim': pagfim}
  try:
    r = requests.post('http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm', data=payload)
  except requests.exceptions.RequestException as e:
    print('An error has occurred. Please try again later.')
    raise SystemExit(e)

  return r

def findMaxRow(html):
  findMaxRow = html.find(text=re.compile('1 a 112 de '))
  if(findMaxRow):
    words = findMaxRow.strip().split()
    return words[-1]
  else:
    return 0

for uf in ufList:
  startRow = 1
  endRow = 112
  page = reqFaixaCep(uf, startRow, endRow)

  # logica para inserir os valores em uma list abaixo e pegar o maxrow do html
  soup = BeautifulSoup(page.text, 'html.parser')
  content = soup.find('div', class_='ctrlcontent')

  maxRow = findMaxRow(content)

  tableRows = content.find_all('tr', attrs={'bgcolor':'#C4DEE9'})

  cepList = []
  for tableRow in tableRows:
    cells = tableRow.findAll('td')
    info = {}

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
    cepList.append(info)
  
  data.update({uf: cepList})

  # while endRow <= maxRow:
  #   startRow = endRow + 1
  #   endRow += qtdRow
  #   page = reqFaixaCep(uf, startRow, endRow)
  #   # logica para inserir os valores em uma list abaixo
  #   print(page.status_code)


print(data)


