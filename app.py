import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

os.environ['FLASK_DEBUG'] = 'True'
app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
def pagina_home():
    return render_template('index.html')


@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')


@app.route('/cadastro')
def glossario():

    glossario_de_termos = []

    with open(
            'bd_candidatos.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    return render_template('cadastro.html',
                           glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    nome = request.form['nome']
    email = request.form['email']
    numero = request.form['numero']
    definicao = request.form['definicao']

    with open(
            'bd_candidatos.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([nome, email, numero, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_candidatos.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break


    with open('bd_candidatos.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))


if __name__ in '__main__':
    app.run()