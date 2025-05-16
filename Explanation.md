# 課題1 Flask クイズアプリ

## Folder構成

```bash
oca-first-flask-app
├─app
│  ├─static
│  ├─templates
│  └─__pycache__
├─mysql
└─nginx
```

## 機能と実装

### 機能
- クイズ
  - 一覧
  - 出題
  - 作成
  - 編集
  - 削除


### 実装方法
- データベース
  MySQLを使用

- 一覧
  一覧データを取得
  `SELECT id, question, answer FROM quiz`

- 作成
  Formから問題と答えのデータを受け取り挿入
  `INSERT INTO quiz (question, answer) VALUES (%s, %s)", (question, answer)`

- 出題
  クイズがない場合、クイズを作成してもらうようにする
  ```python
  if not quizzes:
    return "クイズがありません<br><a href='/create'>クイズを作成する</a>"
  ```
  クイズをランダムに出題
  `quiz = random.choice(quizzes)`
  正解・不正解の判定
  比較しbool形式で正解(True)不正解(False)を返す
  `correct = quiz['answer'].strip() == user_answer`

- 編集
  一覧画面でそれぞれのクイズに`/edit/id`の形にして、編集ボタンを押したら編集画面に特定のクイズを表示
  `SELECT id, question, answer FROM quiz WHERE id=%s", (id,)`
  編集内容を受け取り更新
  `UPDATE quiz SET question=%s, answer=%s WHERE id=%s", (question, answer, id)`

- 削除
  編集と同様に`/delete/id`の形で送信すると削除
  `DELETE FROM quiz WHERE id=%s", (id,)`
  