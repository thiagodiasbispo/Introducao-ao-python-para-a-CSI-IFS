def exportar_servidores_para_csv(servidores, nome_arquivo):
  colunas = ("id", 
            "nome", 
            "situacao_servidor", 
            "unidade_exercicio", 
            "cargo", 
            "classe_cargo", 
            "padrao_cargo"
  )

  with open(nome_arquivo, "w") as f:
    writer = csv.writer(f, delimiter = ";")
    writer.writerow(colunas)

    for servidor in servidores:
      info_servidor = (servidor[c] for c in colunas)
      writer.writerow(info_servidor)
