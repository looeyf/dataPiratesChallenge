import requests
import re
from bs4 import BeautifulSoup

qtdRow = 112 # nr maximo de rows por requisicao

def reqFaixaCep(uf, pagini, pagfim):
  payload = {'UF': uf, 'qtdrow': qtdRow, 'pagini': pagini, 'pagfim': pagfim}
  try:
    r = requests.post('http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm', data=payload)
  except requests.exceptions.RequestException as e:
    print('An error has occurred. Please try again later.')
    raise SystemExit(e)

  return r

def findMaxRow(html):
  findMaxRow = html.find(text=re.compile('1 a 112 de '))
  words = findMaxRow.strip().split()
  return words[-1]

# ufList = ['RS', 'SC']
ufList = ['RS']

for uf in ufList:
  startRow = 1
  endRow = 112
  page = reqFaixaCep(uf, startRow, endRow)

  # logica para inserir os valores em uma list abaixo e pegar o maxrow do html
  soup = BeautifulSoup(page.text, 'html.parser')
  content = soup.find('div', class_='ctrlcontent')

  maxRow = findMaxRow(content)

  tableRows = content.find_all('tr', attrs={'bgcolor':'#C4DEE9'})

  for tableRow in tableRows:
    cells = tableRow.findAll('td')
    for cell in cells:
      print(cell.text.strip())


  # while endRow <= maxRow:
  #   startRow = endRow + 1
  #   endRow += qtdRow
  #   page = reqFaixaCep(uf, startRow, endRow)
  #   # logica para inserir os valores em uma list abaixo
  #   print(page.status_code)


