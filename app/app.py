from flask import Flask, render_template, request, redirect
import mysql.connector
import random

app = Flask(__name__)

# MySQL 接続設定
def get_connection():
  return mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="quiz_db",
    charset='utf8mb4'
  )

@app.route('/')
def index():
  return redirect('/list')

# クイズ作成
@app.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    question = request.form['question']
    answer = request.form['answer']
    conn = get_connection()
    cursor = conn.cursor(prepared=True)
    cursor.execute("INSERT INTO quiz (question, answer) VALUES (%s, %s)", (question, answer))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/list')
  return render_template('create.html')

# 一覧表示
@app.route('/list')
def list_quizzes():
  conn = get_connection()
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT id, question, answer FROM quiz")
  quizzes = cursor.fetchall()
  cursor.close()
  conn.close()
  return render_template('list.html', quizzes=quizzes)

# 編集
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  conn = get_connection()
  cursor = conn.cursor(prepared=True)

  if request.method == 'POST':
    question = request.form['question']
    answer = request.form['answer']
    cursor.execute("UPDATE quiz SET question=%s, answer=%s WHERE id=%s", (question, answer, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/list')

  cursor.execute("SELECT id, question, answer FROM quiz WHERE id=%s", (id,))
  quiz = cursor.fetchone()
  cursor.close()
  conn.close()
  return render_template('create.html', quiz={'id': quiz[0], 'question': quiz[1], 'answer': quiz[2]})

# 削除
@app.route('/delete/<int:id>')
def delete(id):
  conn = get_connection()
  cursor = conn.cursor(prepared=True)
  cursor.execute("DELETE FROM quiz WHERE id=%s", (id,))
  conn.commit()
  cursor.close()
  conn.close()
  return redirect('/list')

# クイズ出題
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
  conn = get_connection()
  cursor = conn.cursor(dictionary=True, prepared=True)

  if request.method == 'POST':
    quiz_id = int(request.form['quiz_id'])
    user_answer = request.form['user_answer'].strip()
    cursor.execute("SELECT answer, question FROM quiz WHERE id=%s", (quiz_id,))
    quiz = cursor.fetchone()
    correct = quiz['answer'].strip() == user_answer
    return render_template('quiz.html', quiz=quiz, result=correct)

  cursor.execute("SELECT * FROM quiz")
  quizzes = cursor.fetchall()
  if not quizzes:
    return "クイズがありません<br><a href='/create'>クイズを作成する</a>"
  quiz = random.choice(quizzes)
  return render_template('quiz.html', quiz=quiz)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3031)