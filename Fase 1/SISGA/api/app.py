from flask import Flask, jsonify, request
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

@app.route('/pessoas/<cpf>', methods=['GET'])
def get_pessoa(cpf=''):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM public.pessoas WHERE cpf = %s;", ([cpf]))
  pessoa = cursor.fetchone()
  cursor.close()
  if pessoa:
    return jsonify(pessoa)
  return jsonify({'error': 'pessoa não encontrado'}), 404

@app.route('/pessoas', methods=['POST'])
def create_pessoa():
  data = request.json
  cursor = conn.cursor()
  cursor.execute("""
    INSERT INTO public.pessoas (
      cpf,
      nome,	
      email,	
      data_nascimento,	
      sexo,	
      cep,	
      telefone
      ) 
      VALUES (%s, %s, %s, %s, %s, %s, %s) 
    RETURNING cpf;
    """, 
    (data['cpf'], data['nome'], data['email'], data['data_nascimento'], data['sexo'], data['cep'], data['telefone']))
  cpf = cursor.fetchone()[0]
  conn.commit()
  cursor.close()
  return jsonify({'cpf': cpf}), 201

@app.route('/pessoas/<cpf>', methods=['PUT'])
def update_pessoa(cpf=''):
  print("chegu")
  data = request.json
  cursor = conn.cursor()
  cursor.execute("""
    UPDATE public.pessoas 
    SET 
      cpf = %s,
      nome = %s,	
      email = %s,	
      data_nascimento = %s,	
      sexo = %s,	
      cep = %s,	
      telefone = %s
    WHERE cpf = %s;
    """, (data['cpf'], data['nome'], data['email'], data['data_nascimento'], data['sexo'], data['cep'], data['telefone'], cpf))
  conn.commit()
  cursor.close()
  return jsonify({'message': 'pessoa atualizado com sucesso'})

@app.route('/pessoas/<cpf>', methods=['DELETE'])
def delete_pessoa(cpf=''):
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





#Auxiliar Alunos
@app.route('/alunospessoas', methods=['GET'])
def get_alunospessoas():
  cursor = conn.cursor()
  cursor.execute("""
                  SELECT 
                    a.cod_aluno,
                    a.cpf,
                    p.nome,
                    p.email,
                    p.data_nascimento,
                    p.sexo,
                    p.cep,
                    p.telefone
                  FROM public.alunos a
                  LEFT JOIN public.pessoas p
                    ON a.cpf = p.cpf
                  ORDER BY a.cod_aluno
                  ;""")
  alunospessoas = cursor.fetchall()
  cursor.close()
  return jsonify(alunospessoas)

@app.route('/alunospessoas/<int:cod_aluno>', methods=['GET'])
def get_alunopessoa(cod_aluno):
  cursor = conn.cursor()
  cursor.execute("""
                  SELECT 
                    a.cod_aluno,
                    a.cpf,
                    p.nome,
                    p.email,
                    p.data_nascimento,
                    p.sexo,
                    p.cep,
                    p.telefone
                  FROM public.alunos a
                  LEFT JOIN public.pessoas p
                    ON a.cpf = p.cpf
                  WHERE
                    a.cod_aluno = %s
                  ;""", (cod_aluno,))
  alunopessoa = cursor.fetchall()
  cursor.close()
  return jsonify(alunopessoa)

@app.route('/alunospessoas', methods=['POST'])
def create_alunospessoas():
  data = request.json
  cursor = conn.cursor()
  cursor.execute("""
    INSERT INTO public.pessoas (
      cpf,
      nome,	
      email,	
      data_nascimento,	
      sexo,	
      cep,	
      telefone
      ) 
      VALUES (%s, %s, %s, %s, %s, %s, %s) 
    RETURNING cpf;
    """, 
    (data['cpf'], data['nome'], data['email'], data['data_nascimento'], data['sexo'], data['cep'], data['telefone']))
  cpf = cursor.fetchone()[0]
  cursor.execute("""
    INSERT INTO public.alunos (
      cpf
      ) 
      VALUES (%s) 
    RETURNING cod_aluno;
    """, 
    (cpf, ))
  cod_aluno = cursor.fetchone()[0]
  
  conn.commit()
  cursor.close()
  
  return jsonify({
    'cpf': cpf,
    'cod_aluno': cod_aluno,
  }), 201



# Cursos
@app.route('/cursos', methods=['GET'])
def get_cursos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.cursos;")
    cursos = cursor.fetchall()
    cursor.close()
    return jsonify(cursos)

@app.route('/cursos/<int:cod_curso>', methods=['GET'])
def get_curso(cod_curso):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.cursos WHERE cod_curso = %s;", (cod_curso,))
    curso = cursor.fetchone()
    cursor.close()
    if curso:
        return jsonify(curso)
    return jsonify({'error': 'Curso não encontrado'}), 404

@app.route('/cursos', methods=['POST'])
def create_curso():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.cursos (nome, periodo, credito_total, cod_coordenador)
        VALUES (%s, %s, %s, %s) RETURNING cod_curso;
    """, (data['nome'], data['periodo'], data['credito_total'], data['cod_coordenador']))
    cod_curso = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'cod_curso': cod_curso}), 201

@app.route('/cursos/<int:cod_curso>', methods=['PUT'])
def update_curso(cod_curso):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE public.cursos 
        SET nome = %s, periodo = %s, credito_total = %s, cod_coordenador = %s 
        WHERE cod_curso = %s;
    """, (data['nome'], data['periodo'], data['credito_total'], data['cod_coordenador'], cod_curso))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Curso atualizado com sucesso'})

@app.route('/cursos/<int:cod_curso>', methods=['DELETE'])
def delete_curso(cod_curso):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.cursos WHERE cod_curso = %s;", (cod_curso,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Curso deletado com sucesso'})





# Disciplinas
@app.route('/disciplinas', methods=['GET'])
def get_disciplinas():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.disciplinas;")
    disciplinas = cursor.fetchall()
    cursor.close()
    return jsonify(disciplinas)

@app.route('/disciplinas/<int:cod_disciplina>', methods=['GET'])
def get_disciplina(cod_disciplina):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.disciplinas WHERE cod_disciplina = %s;", (cod_disciplina,))
    disciplina = cursor.fetchone()
    cursor.close()
    if disciplina:
        return jsonify(disciplina)
    return jsonify({'error': 'Disciplina não encontrada'}), 404

@app.route('/disciplinas', methods=['POST'])
def create_disciplina():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.disciplinas (nome, fase, creditos)
        VALUES (%s, %s, %s) RETURNING cod_disciplina;
    """, (data['nome'], data['fase'], data['creditos']))
    cod_disciplina = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'cod_disciplina': cod_disciplina}), 201

@app.route('/disciplinas/<int:cod_disciplina>', methods=['PUT'])
def update_disciplina(cod_disciplina):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE public.disciplinas 
        SET nome = %s, fase = %s, creditos = %s 
        WHERE cod_disciplina = %s;
    """, (data['nome'], data['fase'], data['creditos'], cod_disciplina))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Disciplina atualizada com sucesso'})

@app.route('/disciplinas/<int:cod_disciplina>', methods=['DELETE'])
def delete_disciplina(cod_disciplina):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.disciplinas WHERE cod_disciplina = %s;", (cod_disciplina,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Disciplina deletada com sucesso'})





# Curso_Disciplinas
@app.route('/curso_disciplinas', methods=['GET'])
def get_curso_disciplinas():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.curso_disciplinas;")
    curso_disciplinas = cursor.fetchall()
    cursor.close()
    return jsonify(curso_disciplinas)

@app.route('/curso_disciplinas', methods=['POST'])
def create_curso_disciplina():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.curso_disciplinas (cod_curso, cod_disciplina)
        VALUES (%s, %s) RETURNING cod_curso, cod_disciplina;
    """, (data['cod_curso'], data['cod_disciplina']))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    return jsonify({'cod_curso': result[0], 'cod_disciplina': result[1]}), 201

@app.route('/curso_disciplinas', methods=['DELETE'])
def delete_curso_disciplina():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.curso_disciplinas WHERE cod_curso = %s AND cod_disciplina = %s;",
                   (data['cod_curso'], data['cod_disciplina']))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Associação curso-disciplina deletada com sucesso'})





# Turmas
@app.route('/turmas', methods=['GET'])
def get_turmas():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.turmas;")
    turmas = cursor.fetchall()
    cursor.close()
    return jsonify(turmas)

@app.route('/turmas/<int:cod_turma>', methods=['GET'])
def get_turma(cod_turma):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.turmas WHERE cod_turma = %s;", (cod_turma,))
    turma = cursor.fetchone()
    cursor.close()
    if turma:
        return jsonify(turma)
    return jsonify({'error': 'Turma não encontrada'}), 404

@app.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.turmas (cod_disciplina, horario, ano, semestre, cod_professor)
        VALUES (%s, %s, %s, %s, %s) RETURNING cod_turma;
    """, (data['cod_disciplina'], data['horario'], data['ano'], data['semestre'], data['cod_professor']))
    cod_turma = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'cod_turma': cod_turma}), 201

@app.route('/turmas/<int:cod_turma>', methods=['PUT'])
def update_turma(cod_turma):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE public.turmas 
        SET cod_disciplina = %s, horario = %s, ano = %s, semestre = %s, cod_professor = %s
        WHERE cod_turma = %s;
    """, (data['cod_disciplina'], data['horario'], data['ano'], data['semestre'], data['cod_professor'], cod_turma))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Turma atualizada com sucesso'})

@app.route('/turmas/<int:cod_turma>', methods=['DELETE'])
def delete_turma(cod_turma):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.turmas WHERE cod_turma = %s;", (cod_turma,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Turma deletada com sucesso'})





# Relatorios

@app.route('/relatorios', methods=['GET'])
def get_relatórios():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.cod_relatorio, a.cod_aluno, array_agg(d.nome) AS disciplinas, r.notas, r.faltas
        FROM public.relatorios r
        JOIN public.alunos a ON r.cod_aluno = a.cod_aluno
        JOIN public.historicos h ON h.cod_aluno = a.cod_aluno
        JOIN public.disciplinas d ON h.cod_disciplina = d.cod_disciplina
        GROUP BY r.cod_relatorio, a.cod_aluno, r.notas, r.faltas;
    """)
    relatorios = cursor.fetchall()
    cursor.close()
    return jsonify(relatorios)

@app.route('/historico/<int:cod_aluno>', methods=['GET'])
def get_historico(cod_aluno):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.nome, h.nota_geral, h.frequencia_geral, h.aprovacao_final
        FROM public.historicos h
        JOIN public.disciplinas d ON h.cod_disciplina = d.cod_disciplina
        WHERE h.cod_aluno = %s;
    """, (cod_aluno,))
    historico = cursor.fetchall()
    cursor.close()
    return jsonify(historico)
    ##novos##
@app.route('/relatorios', methods=['GET'])
def get_relatorios():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.relatorios;")
    relatorios = cursor.fetchall()
    cursor.close()
    return jsonify(relatorios)

@app.route('/relatorios/<int:cod_relatorio>', methods=['GET'])
def get_relatorio(cod_relatorio):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.relatorios WHERE cod_relatorio = %s;", (cod_relatorio,))
    relatorio = cursor.fetchone()
    cursor.close()
    if relatorio:
        return jsonify(relatorio)
    return jsonify({'error': 'Relatório não encontrado'}), 404

@app.route('/relatorios', methods=['POST'])
def create_relatorio():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.relatorios (cod_aluno, cod_turma, conteudo, data_envio)
        VALUES (%s, %s, %s, %s) RETURNING cod_relatorio;
    """, (data['cod_aluno'], data['cod_turma'], data['conteudo'], data['data_envio']))
    cod_relatorio = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'cod_relatorio': cod_relatorio}), 201

@app.route('/relatorios/<int:cod_relatorio>', methods=['PUT'])
def update_relatorio(cod_relatorio):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE public.relatorios 
        SET cod_aluno = %s, cod_turma = %s, conteudo = %s, data_envio = %s
        WHERE cod_relatorio = %s;
    """, (data['cod_aluno'], data['cod_turma'], data['conteudo'], data['data_envio'], cod_relatorio))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Relatório atualizado com sucesso'})

@app.route('/relatorios/<int:cod_relatorio>', methods=['DELETE'])
def delete_relatorio(cod_relatorio):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.relatorios WHERE cod_relatorio = %s;", (cod_relatorio,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Relatório deletado com sucesso'})





# Historicos
@app.route('/historicos', methods=['GET'])
def get_historicos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.historicos;")
    historicos = cursor.fetchall()
    cursor.close()
    return jsonify(historicos)

@app.route('/historicos/<int:cod_historico>', methods=['GET'])
def get_historico(cod_historico):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.historicos WHERE cod_historico = %s;", (cod_historico,))
    historico = cursor.fetchone()
    cursor.close()
    if historico:
        return jsonify(historico)
    return jsonify({'error': 'Histórico não encontrado'}), 404

@app.route('/historicos', methods=['POST'])
def create_historico():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.historicos (cod_aluno, cod_turma, nota, frequencia, status)
        VALUES (%s, %s, %s, %s, %s) RETURNING cod_historico;
    """, (data['cod_aluno'], data['cod_turma'], data['nota'], data['frequencia'], data['status']))
    cod_historico = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'cod_historico': cod_historico}), 201

@app.route('/historicos/<int:cod_historico>', methods=['PUT'])
def update_historico(cod_historico):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE public.historicos 
        SET cod_aluno = %s, cod_turma = %s, nota = %s, frequencia = %s, status = %s
        WHERE cod_historico = %s;
    """, (data['cod_aluno'], data['cod_turma'], data['nota'], data['frequencia'], data['status'], cod_historico))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Histórico atualizado com sucesso'})

@app.route('/historicos/<int:cod_historico>', methods=['DELETE'])
def delete_historico(cod_historico):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.historicos WHERE cod_historico = %s;", (cod_historico,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Histórico deletado com sucesso'})




#intercessão
@app.route('/alunos_disciplinas', methods=['GET'])
def get_alunos_disciplinas():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.cod_aluno, p.nome AS aluno_nome, d.nome AS disciplina_nome
        FROM public.alunos a
        JOIN public.historicos h ON a.cod_aluno = h.cod_aluno
        JOIN public.disciplinas d ON h.cod_disciplina = d.cod_disciplina
        JOIN public.pessoas p ON a.cpf = p.cpf;
    """)
    alunos_disciplinas = cursor.fetchall()
    cursor.close()
    return jsonify(alunos_disciplinas)

@app.route('/coordenadores_cursos', methods=['GET'])
def get_coordenadores_cursos():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.cod_coordenador, p.nome AS coordenador_nome, cu.nome AS curso_nome
        FROM public.coordenadores c
        JOIN public.cursos cu ON c.cod_coordenador = cu.cod_coordenador
        JOIN public.pessoas p ON c.cpf = p.cpf;
    """)
    coordenadores_cursos = cursor.fetchall()
    cursor.close()
    return jsonify(coordenadores_cursos)

@app.route('/professores_disciplinas', methods=['GET'])
def get_professores_disciplinas():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pr.cod_professor, p.nome AS professor_nome, d.nome AS disciplina_nome
        FROM public.professores pr
        JOIN public.turmas t ON pr.cod_professor = t.cod_professor
        JOIN public.disciplinas d ON t.cod_disciplina = d.cod_disciplina
        JOIN public.pessoas p ON pr.cpf = p.cpf;
    """)
    professores_disciplinas = cursor.fetchall()
    cursor.close()
    return jsonify(professores_disciplinas)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5002)