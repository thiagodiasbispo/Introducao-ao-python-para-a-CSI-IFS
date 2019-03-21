# -*- coding: utf-8 -*-

import sqlite3 as sqlite

class EmailAcademico():
    def __init__(self, nome, email, cpf, nascimento):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.nascimento = nascimento
    
    def __str__(self):  
        return f"{self.nome}: {self.email}"
    
    def __repr__(self):  
        return str(self)


class EmailAcademicoDao():
    SQL_LISTAR_TODOS = """
        SELECT 
                    nome,
                    email,
                    cpf,
                    nascimento 
                FROM email_academico
    """
    SQL_GET_POR_CPF = """
        SELECT 
            nome,
            email,
            cpf,
            nascimento 
            FROM email_academico 
            WHERE cpf = ?
    """

    SQL_UPDATE = """
        UPDATE email_academico 
            SET nome=?, email=?, nascimento= ? 
        WHERE cpf = ?
    """
          
    SQL_DELETE = """
        DELETE FROM email_academico where cpf = ?
    
    """
    def __init__(self, db_file):
        self.db_file = db_file
        
    def _connection(self):
        return sqlite.connect(self.db_file)
    
    def executar_sql(self, sql, params = ()):
        conn = self._connection()
        cursor = conn.cursor()
        return cursor.execute(sql, params)

    def listar_todos(self):
        return map(self._to_email_academico, 
                   self.executar_sql(self.SQL_LISTAR_TODOS))
        
        
    def _to_email_academico(self, raw):
        if raw:
            return EmailAcademico(*raw)
        # Não é necessário escrever a cláusula else, uma vez que se não explicitarmos o retorno de uma função ou método python, seu retorno será "None"

    
    def get(self, pk):
        raw = self.executar_sql(self.SQL_GET_POR_CPF, (pk,)).fetchone()
        return self._to_email_academico(raw)
    
    def update(self, a):
        conn = self._connection()
        cursor = conn.cursor()
        res = cursor.execute(self.SQL_UPDATE, (a.nome, a.email, a.nascimento, a.cpf)) #Atualizando todos os campos de uma vez só, uma vez que não sabemos qual foi alterado
        conn.commit()
    
    def delete(self, pk):
        if not pk:
            raise Exception ("Informe a chave-primária")
        conn = self._connection()
        cursor = conn.cursor()
        res = cursor.execute(self.SQL_DELETE, (pk,)) #Precisamos passar um valor iterável como argumento, uma vez que é isso que o método "execute" espera
        
        conn.commit()

        
            
        
        

def main():
    dao = EmailAcademicoDao("./db.sqlite3")
     res = dao.listar_todos()
    for email in dao.listar_todos():
        print(email) 

    

if __name__ == "__main__":
    main()