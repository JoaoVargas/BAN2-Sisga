from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from connection import get_conn
conn = get_conn()

app = Flask(__name__)
CORS(app)

########################################Alunos####################################################
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

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"success": "okay"})

@app.route('/inicializar', methods=['GET'])
def inicializar():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM alunos")
        print(cursor.fetchall())
        return jsonify(cursor.fetchall())
############################Coordenadores#######################################
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

############################Professores#######################################
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


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5002)