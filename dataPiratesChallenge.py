import requests

qtdRow = 112 # nr maximo de rows por requisicao

def reqFaixaCep(uf, pagini, pagfim):
  payload = {"UF": uf, "qtdrow": qtdRow, "pagini": pagini, "pagfim": pagfim}
  r = requests.post("http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm", data=payload)
  return r

# ufList = ['RS', 'SC']
ufList = ['RS']

for uf in ufList:
  startRow = 1
  endRow = 112
  value = reqFaixaCep(uf, startRow, endRow)
  # logica para inserir os valores em uma list abaixo e pegar o maxrow do html
  print(value.status_code)

  maxRow = 534 #aqui vou atualizar o valor do maxRow pegando de dentro do html


  while endRow <= maxRow:
    startRow = endRow + 1
    endRow += qtdRow
    value = reqFaixaCep(uf, startRow, endRow)
    # logica para inserir os valores em uma list abaixo
    print(value.status_code)


