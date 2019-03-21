def clean_cpf(cpf):
	"""
		Método de limpeza do CPF, reponsável por eliminar os sinais usados para sua formatação.
	"""
  if not isinstance(cpf, str):
    cpf = str(cpf)
  digits = tuple(cpf)
  only_numbers = (c for c in digits if c.isdigit())
  return ''.join(only_numbers)