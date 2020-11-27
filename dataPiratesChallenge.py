import requests

def reqFaixaCep(uf):
  payload = {"UF": uf, "Localidade": "", "qtdrow": 112}
  r = requests.post("http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm", data=payload)
  return r

ufList = ['RS', 'SC']

for uf in ufList:
  value = reqFaixaCep(uf)
  print(value.status_code)

