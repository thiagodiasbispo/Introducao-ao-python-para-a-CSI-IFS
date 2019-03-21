
from flask import Flask, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth

from util import clean_cpf
from db import DBAccess, AlunoNaoEncontradoException

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	"""
		Resposta retornada quando o usuário da API informa um CPF inválido ou inexistente em nossa base de dados.
	"""
    return make_response(jsonify({'Alerta': 'Aluno nao encontrado ou entrada invalida'}), 404)

@app.route('/egressos/api/v1.0/aptidao/<int:cpf>', methods=['GET'])
#@auth.login_required
def aptidao(cpf):
    cpf = clean_cpf(cpf)
    try:
      aptidao = DBAccess.aluno_esta_matriculado(clean_cpf(cpf))
      return jsonify({'aptidao':  aptidao}) # Retorna "True" caso aluno esteja matriculado ou cadastrado (fase anterior à metrícula) no IFS
    except AlunoNaoEncontradoException as e:
      abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='3000')