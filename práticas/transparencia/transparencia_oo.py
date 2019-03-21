"""
  Módulo ainda não terminado. 

  O objetivo dele é demonstrar como implementar as mesmas funcionalidades do módulo "transparenci_imp" através da Orientação a Objetos do Python
"""
class Servidor():

  def __init__(self, id_, nome, situacao_servidor, unidade_exercicio, cargo, classe_cargo, padrao_cargo):

    self.id = id_
    self.nome = nome
    self.situacao_servidor=situacao_servidor
    self.unidade_exercicio=unidade_exercicio
    self.cargo=cargo
    self.classe_cargo=classe_cargo
    self.padrao_cargo=padrao_cargo

  def __str__(self):
    return "{} ({}): {}".format(self.nome, self.id, self.unidade_exercicio)
  
  @staticmethod
  def from_json(dict_servidor):
    """
      Cria um objeto do tipo Servidor a partir do acesso ao endpoint "/api-de-dados/servidores" servidor do portal da transparência.

      param dict_servidor: Dicionário contendo todos os dados do servidor

      return: Objeto do tipo Servidor
    """

      servidor = dict_servidor["servidor"]
      ficha = dict_servidor["fichasCargoEfetivo"][0]

      return Servidor(
          id_=servidor["id"],
          nome=servidor["pessoa"]["nome"],
          situacao_servidor=ficha["situacaoServidor"],
          unidade_exercicio=ficha["uorgExercicio"],
          cargo= ficha["cargo"],
          classe_cargo=ficha["classeCargo"],
          padrao_cargo=ficha["padraoCargo"]
      )

    except Exception as e:
      print(e)
      raise e

def main():
    s = Servidor(999, "Thiago", "ATIVO PERMANENTE","CSI","TEC. LAB", "D", "405")
    print(s)

if __name__ == "__main__":
  main()