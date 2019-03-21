import requests
import itertools
from pprint import pprint
import json
import csv

import util

CODIGO_IFS = "26423"
URL_BASE = "http://www.transparencia.gov.br"
END_POINT_SERVIDORES = "/api-de-dados/servidores"

PARAMETROS_BUSCA_IFS = {"orgaoServidorExercicio": CODIGO_IFS}

#http://www.transparencia.gov.br/swagger-ui.html#!/Servidores32do32Poder32Executivo32Federal/dadosServidoresUsingGET



def obter_servidores(dados_completos):
  for dado in dados_completos:
    try:
      servidor = dado["servidor"]
      ficha = dado["fichasCargoEfetivo"][0]

      yield {
          "id": servidor["id"],
          "nome": servidor["pessoa"]["nome"],
          "situacao_servidor": ficha["situacaoServidor"],
          "unidade_exercicio": ficha["uorgExercicio"],
          "cargo": ficha["cargo"],
          "classe_cargo": ficha["classeCargo"],
          "padrao_cargo": ficha["padraoCargo"]
      } 

    except Exception as e:
      print(e)


def executar_consulta(url, params={}):
    response = requests.get(url, params=params)
    return response.json()

def montar_url(end_point):
    return "{}{}".format(URL_BASE, end_point)

def montar_url_servidores_ifs():
    return montar_url(END_POINT_SERVIDORES)

def listar_todos(paginas_de = (1, None)):
    inicio, fim = paginas_de
    
    if not fim:
      intervalo_paginas = itertools.count(inicio)
    else:
      intervalo_paginas = range(inicio, fim+1)
    
    url = montar_url_servidores_ifs()
    params = dict(PARAMETROS_BUSCA_IFS)

    print("URL montada...")
    print("Listando servidores...")

    for pagina in intervalo_paginas:
      print("Página {:03d}...".format(pagina))

      params["pagina"] = pagina
      try:
        print("Consultando próximos servidores...")
        dados = executar_consulta(url, params)
      except Exception as e:
        print(e)
        break

      for servidor in obter_servidores(dados):
        yield servidor


def save_json(nome_arquivo, dados):
  with open(nome_arquivo, "w") as f:
    json.dump(dados, f, indent="\t")

def main():
  servidores = listar_todos((36, 100))
  print("Exportando servidores...")
  util.exportar_servidores_para_csv(servidores, "./servidores_imp.csv")
  print("Sucesso!")

if __name__ == "__main__":
  main()