import sqlite3 as sqlite
import os
from random import choice
import csv

import util

class DBAccess():
  FILES_PATH =  os.path.join(os.path.dirname(__file__),"files") # O método "os.path.join" une seus parâmetros com o separador de diretório do sistema operacional
  DB_FILE_NAME = os.path.join(FILES_PATH, "academico.db")

  @classmethod
  def listar_todos(cls):
    cursor = DBAccess.get_connection().cursor()
    for row in cursor.execute("select * from alunos"):
      yield row  

    cursor.close()
  
  @staticmethod
  def aluno_esta_matriculado(cpf):
    cpf = util.clean_cpf(cpf)
    sql = "select situacao from alunos where cpf = ?;"

    cursor = DBAccess.get_connection().cursor()
    data = cursor.execute(sql, (cpf,)).fetchone()

    if not data: # Se nenhum aluno for encontrado, retorna uma exceção
      raise AlunoNaoEncontradoException()
    
    situacao = data[0]

    return situacao in ("MATRICULADO", "CADASTRADO") # O aluno está na situação "cadastrado"  quando passou no processo seletivo mas ainda não foi matriculado pela Instituição
    


  @classmethod
  def get_connection(cls):
    return sqlite.connect(cls.DB_FILE_NAME)

  @classmethod
  def _create_db(cls):
    try:
      conn = sqlite.connect(cls.DB_FILE_NAME)
      print("sqlite version: {} ".format(sqlite.version))
    except Error as e:
      print(e)
    finally:
      conn.close() 
  
  @classmethod
  def _create_tables(cls):
    create_table_alunos_file = os.path.join(cls.FILES_PATH, "create_alunos_table.sql")

    with open(create_table_alunos_file) as f:
      sql = f.read()

    conn = cls.get_connection()
    conn.execute(sql)
  
  @classmethod
  def _insert_initial_data(cls):
    init_data_file = os.path.join(cls.FILES_PATH, "init.csv")

    situacoes_possiveis = ("CONCLUIDO", "EVADIDO", "CADASTRADO" , "MATRICULADO")

    initial_data = []

    with open(init_data_file) as f:
      reader = csv.reader(f, delimiter=";")
      next(reader) #Consideramos que a primeira linha do csv com os dados de exemplo seja o cabeçalho, por isso ela é descartada
      initial_data = [data for data in reader] #Lemos todos os dados de uma vez para permitir fechar o arquivo antes de iniciar a conexão com a base de dados.
    
    sql_template = "INSERT INTO alunos (nome, cpf, situacao) VALUES (?,?,?);"

    conn = cls.get_connection()
    cursor = conn.cursor()

    data_to_insert = [
      (nome, util.clean_cpf(cpf), choice(situacoes_possiveis)) # O método "choice" (módulo random) escolhe aleatoriamente um item do iterável recebido como parâmetro
        for nome, cpf in initial_data
    ]

    cursor.executemany(sql_template, data_to_insert)
    conn.commit()
    cursor.close()
    
     
  @classmethod
  def init(cls):
    """
      Função auxiliar usada para criar inicializar a base de dados.
      Só executa os procedimentos caso o arquivo da base não exista.
    """

    if not os.path.exists(cls.DB_FILE_NAME):
      cls._create_db()
      cls._create_tables()
      cls._insert_initial_data()
  
class AlunoNaoEncontradoException(Exception):
  """
    Classe auxiliar para facilitar a notificação de quando o aluno pesquisado através de seu cpf informado não é encontrado.
  """
  def __init__(self):
    super(Exception, self).__init__("Aluno não encontrado")


