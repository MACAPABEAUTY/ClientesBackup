
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'segredo'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def get_db_connection():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha)).fetchone()
    conn.close()
    if user:
        session['usuario'] = usuario
        return redirect(url_for('dashboard'))
    flash('Usuário ou senha inválido!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    dados = conn.execute('SELECT * FROM backup_status ORDER BY data DESC').fetchall()
    conn.close()
    return render_template('painel.html', dados=dados, usuario=session['usuario'])

if __name__ == '__main__':
    app.run(debug=True)
