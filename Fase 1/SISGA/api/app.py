from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import datetime as dt
import json

from connection import get_conn
conn = get_conn()

app = Flask(__name__)
CORS(app)





# Sistema
@app.route('/', methods=['GET'])
def health_check():
  return jsonify({"message": "Healthy"})

@app.route('/inicializar', methods=['GET'])
def inicializar():
  with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM pessoas")
    pessoas =cursor.fetchall()
  with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM disciplinas")
    disciplinas =cursor.fetchall()
      
  if len(pessoas) != 0 and len(disciplinas) != 0:
    return jsonify({'error': 'Banco já inicializado'})
  
  with open('./inicializador.json', 'r') as file:
    data = json.load(file)
  
  for pessoa in data["pessoas"]:
    with conn.cursor() as cursorpessoa:
      cursorpessoa.execute(
        """INSERT INTO public.pessoas (
        cpf, 
        nome, 
        sexo, 
        cep, 
        email, 
        data_nascimento, 
        telefone
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        RETURNING cpf;
        """,
        (
        pessoa["cpf"], 
        pessoa["nome"], 
        pessoa["sexo"], 
        pessoa["cep"], 
        pessoa["email"],
        dt.datetime.strptime(pessoa["data_nascimento"], '%d/%m/%Y').date(),
        pessoa["telefone"]
        )
      )
      pessoa = cursorpessoa.fetchone()[0]
      print(pessoa)
      conn.commit()
      cursorpessoa.close()
  
  for coordenador in data["coordenadores"]:
    with conn.cursor() as cursorcoordenador:
      cursorcoordenador.execute(
        """INSERT INTO public.coordenadores (
        cpf, 
        salario
        ) 
        VALUES (%s, %s) 
        RETURNING cod_coordenador;
        """,
        (
        coordenador["cpf"], 
        coordenador["salario"]
        )
      )
      coordenador = cursorcoordenador.fetchone()[0]
      print(coordenador)
      conn.commit()
      cursorcoordenador.close()
  
  for professor in data["professores"]:
    with conn.cursor() as cursorprofessor:
      cursorprofessor.execute(
        """INSERT INTO public.professores (
        cpf, 
        salario,
        formacao
        ) 
        VALUES (%s, %s, %s) 
        RETURNING cod_professor;
        """,
        (
        professor["cpf"], 
        professor["salario"],
        professor["formacao"]
        )
      )
      professor = cursorprofessor.fetchone()[0]
      print(professor)
      conn.commit()
      cursorprofessor.close()
  
  for aluno in data["alunos"]:
    with conn.cursor() as cursoraluno:
      cursoraluno.execute(
        """INSERT INTO public.alunos (
        cpf
        ) 
        VALUES (%s) 
        RETURNING cod_aluno;
        """,
        (
        [aluno["cpf"]] # quando só tem um item precisa settar como array
        )
      )
      aluno = cursoraluno.fetchone()[0]
      print(aluno)
      conn.commit()
      cursoraluno.close()
  
  for curso in data["cursos"]:
    with conn.cursor() as cursorcurso:
      cursorcurso.execute(
        """INSERT INTO public.cursos (
        nome,
        periodo,
        credito_total,
        cod_coordenador
        ) 
        VALUES (%s, %s, %s, %s) 
        RETURNING cod_curso;
        """,
        (
        curso["nome"], 
        curso["periodo"],
        curso["credito_total"],
        curso["cod_coordenador"]
        )
      )
      curso = cursorcurso.fetchone()[0]
      print(curso)
      conn.commit()
      cursorcurso.close()
  
  for disciplina in data["disciplinas"]:
    with conn.cursor() as cursordisciplina:
      cursordisciplina.execute(
        """INSERT INTO public.disciplinas (
        nome,
        fase,
        creditos
        ) 
        VALUES (%s, %s, %s) 
        RETURNING cod_disciplina;
        """,
        (
        disciplina["nome"], 
        disciplina["fase"],
        disciplina["creditos"]
        )
      )
      disciplina = cursordisciplina.fetchone()[0]
      print(disciplina)
      conn.commit()
      cursordisciplina.close()
  
  for curso_disciplina in data["curso_disciplinas"]:
    with conn.cursor() as cursorcurso_disciplina:
      cursorcurso_disciplina.execute(
        """INSERT INTO public.curso_disciplinas (
        cod_curso,
        cod_disciplina
        ) 
        VALUES (%s, %s) 
        RETURNING cod_curso_disciplina;
        """,
        (
        curso_disciplina["cod_curso"], 
        curso_disciplina["cod_disciplina"]
        )
      )
      curso_disciplina = cursorcurso_disciplina.fetchone()[0]
      print(curso_disciplina)
      conn.commit()
      cursorcurso_disciplina.close()
  
  for turma in data["turmas"]:    
    with conn.cursor() as cursorturma:
      cursorturma.execute(
        """INSERT INTO public.turmas (
        cod_disciplina,
        cod_professor,
        sala,
        max_alunos,
        agenda
        ) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING cod_turma;
        """,
        (
        turma["cod_disciplina"], 
        turma["cod_professor"], 
        turma["sala"], 
        turma["max_alunos"], 
        json.dumps(turma["agenda"], ensure_ascii=False)
        )
      )
      turma = cursorturma.fetchone()[0]
      print(turma)
      conn.commit()
      cursorturma.close()
  
  for relatorio in data["relatorios"]:    
    with conn.cursor() as cursorrelatorio:
      cursorrelatorio.execute(
        """INSERT INTO public.relatorios (
        cod_aluno,
        cod_turma,
        notas,
        faltas
        ) 
        VALUES (%s, %s, %s::real[], %s::date[]) 
        RETURNING cod_relatorio;
        """,
        (
        relatorio["cod_aluno"], 
        relatorio["cod_turma"], 
        relatorio["notas"], 
        relatorio["faltas"]
        )
      )
      relatorio = cursorrelatorio.fetchone()[0]
      print(relatorio)
      conn.commit()
      cursorrelatorio.close()
  
  for historico in data["historicos"]:    
    with conn.cursor() as cursorhistorico:
      cursorhistorico.execute(
        """INSERT INTO public.historicos (
        cod_aluno,
        cod_disciplina,
        nota_geral,
        frequencia_geral,
        aprovacao_final
        ) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING cod_historico;
        """,
        (
        historico["cod_aluno"], 
        historico["cod_disciplina"], 
        historico["nota_geral"], 
        historico["frequencia_geral"], 
        historico["aprovacao_final"]
        )
      )
      historico = cursorhistorico.fetchone()[0]
      print(historico)
      conn.commit()
      cursorhistorico.close()
      
      
    
      
  return jsonify({'message': 'Banco inicializado com sucesso'})





# Pessoas
@app.route('/pessoas', methods=['GET'])
def get_pessoas():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.pessoas;")
  pessoas = cursor.fetchall()
  cursor.close()
  return jsonify(pessoas)

@app.route('/pessoas/<int:cpf>', methods=['GET'])
def get_pessoa(cpf):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.pessoas WHERE cpf = %s;", (cpf,))
  pessoa = cursor.fetchone()
  cursor.close()
  if pessoa:
    return jsonify(pessoa)
  return jsonify({'error': 'pessoa não encontrado'}), 404

@app.route('/pessoas', methods=['POST'])
def create_pessoa():
  data = request.json
  cursor = conn.cursor()
  cursor.execute("INSERT INTO public.pessoas (cpf) VALUES (%s) RETURNING cpf;", (data['cpf'],))
  cpf = cursor.fetchone()[0]
  conn.commit()
  cursor.close()
  return jsonify({'cpf': cpf}), 201

@app.route('/pessoas/<int:cpf>', methods=['PUT'])
def update_pessoa(cpf):
  data = request.json
  cursor = conn.cursor()
  cursor.execute("UPDATE public.pessoas SET cpf = %s WHERE cpf = %s;", (data['cpf'], cpf))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'pessoa atualizado com sucesso'})

@app.route('/pessoas/<int:cpf>', methods=['DELETE'])
def delete_pessoa(cpf):
  cursor = conn.cursor()
  cursor.execute("DELETE FROM public.pessoas WHERE cpf = %s;", (cpf,))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'pessoa deletadado com sucesso'})





# Coordenadores
@app.route('/coordenadores', methods=['GET'])
def get_coordenadores():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.coordenadores;")
  coordenadores = cursor.fetchall()
  cursor.close()
  return jsonify(coordenadores)

@app.route('/coordenadores/<int:cod_coordenador>', methods=['GET'])
def get_coordenador(cod_coordenador):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.coordenadores WHERE cod_coordenador = %s;", (cod_coordenador,))
  coordenador = cursor.fetchone()
  cursor.close()
  if coordenador:
    return jsonify(coordenador)
  return jsonify({'error': 'Coordenador não encontrado'}), 404

@app.route('/coordenadores', methods=['POST'])
def create_coordenador():
  data = request.json
  cursor = conn.cursor()
  cursor.execute(
    "INSERT INTO public.coordenadores (cpf, salario) VALUES (%s, %s) RETURNING cod_coordenador;",
    (data['cpf'], data['salario'])
  )
  cod_coordenador = cursor.fetchone()[0]
  conn.commit()
  cursor.close()
  return jsonify({'cod_coordenador': cod_coordenador}), 201

@app.route('/coordenadores/<int:cod_coordenador>', methods=['PUT'])
def update_coordenador(cod_coordenador):
  data = request.json
  cursor = conn.cursor()
  cursor.execute(
    "UPDATE public.coordenadores SET cpf = %s, salario = %s WHERE cod_coordenador = %s;",
    (data['cpf'], data['salario'], cod_coordenador)
  )
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Coordenador atualizado com sucesso'})

@app.route('/coordenadores/<int:cod_coordenador>', methods=['DELETE'])
def delete_coordenador(cod_coordenador):
  cursor = conn.cursor()
  cursor.execute("DELETE FROM public.coordenadores WHERE cod_coordenador = %s;", (cod_coordenador,))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Coordenador deletadado com sucesso'})





# Professores
@app.route('/professores', methods=['GET'])
def get_professores():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.professores;")
  professores = cursor.fetchall()
  cursor.close()
  return jsonify(professores)

@app.route('/professores/<int:cod_professor>', methods=['GET'])
def get_professor(cod_professor):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.professores WHERE cod_professor = %s;", (cod_professor,))
  professor = cursor.fetchone()
  cursor.close()
  if professor:
    return jsonify(professor)
  return jsonify({'error': 'Professor não encontrado'}), 404

@app.route('/professores', methods=['POST'])
def create_professor():
  data = request.json
  cursor = conn.cursor()
  cursor.execute(
    "INSERT INTO public.professores (cpf, salario, formacao) VALUES (%s, %s, %s) RETURNING cod_professor;",
    (data['cpf'], data['salario'], data.get('formacao'))
  )
  cod_professor = cursor.fetchone()[0]
  conn.commit()
  cursor.close()
  return jsonify({'cod_professor': cod_professor}), 201

@app.route('/professores/<int:cod_professor>', methods=['PUT'])
def update_professor(cod_professor):
  data = request.json
  cursor = conn.cursor()
  cursor.execute(
    "UPDATE public.professores SET cpf = %s, salario = %s, formacao = %s WHERE cod_professor = %s;",
    (data['cpf'], data['salario'], data.get('formacao'), cod_professor)
  )
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Professor atualizado com sucesso'})

@app.route('/professores/<int:cod_professor>', methods=['DELETE'])
def delete_professor(cod_professor):
  cursor = conn.cursor()
  cursor.execute("DELETE FROM public.professores WHERE cod_professor = %s;", (cod_professor,))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Professor deletadado com sucesso'})





# Alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.alunos;")
  alunos = cursor.fetchall()
  cursor.close()
  return jsonify(alunos)

@app.route('/alunos/<int:cod_aluno>', methods=['GET'])
def get_aluno(cod_aluno):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.alunos WHERE cod_aluno = %s;", (cod_aluno,))
  aluno = cursor.fetchone()
  cursor.close()
  if aluno:
    return jsonify(aluno)
  return jsonify({'error': 'Aluno não encontrado'}), 404

@app.route('/alunos', methods=['POST'])
def create_aluno():
  data = request.json
  cursor = conn.cursor()
  cursor.execute("INSERT INTO public.alunos (cpf) VALUES (%s) RETURNING cod_aluno;", (data['cpf'],))
  cod_aluno = cursor.fetchone()[0]
  conn.commit()
  cursor.close()
  return jsonify({'cod_aluno': cod_aluno}), 201

@app.route('/alunos/<int:cod_aluno>', methods=['PUT'])
def update_aluno(cod_aluno):
  data = request.json
  cursor = conn.cursor()
  cursor.execute("UPDATE public.alunos SET cpf = %s WHERE cod_aluno = %s;", (data['cpf'], cod_aluno))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Aluno atualizado com sucesso'})

@app.route('/alunos/<int:cod_aluno>', methods=['DELETE'])
def delete_aluno(cod_aluno):
  cursor = conn.cursor()
  cursor.execute("DELETE FROM public.alunos WHERE cod_aluno = %s;", (cod_aluno,))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'Aluno deletadado com sucesso'})





if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5002)