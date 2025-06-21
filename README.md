# Flask クイズアプリ

## フォルダ構成

```bash
oca-first-flask-app
├─app
│  ├─app.py           # メインのFlaskアプリケーションファイル
│  ├─static           # 静的ファイル（CSS、JavaScript、画像など）を格納するフォルダ
│  ├─templates        # HTMLテンプレートを格納するフォルダ
│  │  ├─create.html   # クイズ作成・編集用のテンプレート
│  │  ├─list.html     # クイズ一覧表示用のテンプレート
│  │  └─quiz.html     # クイズ出題用のテンプレート
│  └─__pycache__      # Pythonのコンパイル済みファイルが格納されるフォルダ
├─mysql               # MySQLデータベースの設定・データファイルを格納するフォルダ
└─nginx               # Nginxの設定ファイルを格納するフォルダ
```

## 機能と実装

### データベース設計
- MySQLを使用してクイズデータを管理
- `quiz_db`データベース内の`quiz`テーブルに問題と回答を保存
- 各クイズは一意のID、問題文（question）、答え（answer）で構成

### 実装した機能

#### 1. クイズ一覧表示（/list）
- すべてのクイズデータをデータベースから取得して表示
- SQL: `SELECT id, question, answer FROM quiz`
- 各クイズに対して編集・削除リンクを表示
- 操作（作成・編集・削除）完了後のメッセージ表示機能

#### 2. クイズ作成（/create）
- フォームから問題と答えのデータを受け取りデータベースに挿入
- SQL: `INSERT INTO quiz (question, answer) VALUES (%s, %s)`
- JavaScript利用で入力チェックと保存前の確認ダイアログを実装
- 問題・回答が空の場合はアラートを表示して送信をキャンセル

#### 3. クイズ編集（/edit/\<id\>）
- 特定IDのクイズデータを取得してフォームに表示
- SQL: `SELECT id, question, answer FROM quiz WHERE id=%s`
- 編集内容を受け取りデータベースを更新
- SQL: `UPDATE quiz SET question=%s, answer=%s WHERE id=%s`
- 作成画面と同じフォームを使用し、編集モードで表示

#### 4. クイズ削除（/delete/\<id\>）
- JavaScript確認ダイアログで削除前に確認
- 特定IDのクイズをデータベースから削除
- SQL: `DELETE FROM quiz WHERE id=%s`

#### 5. クイズ出題・回答判定（/quiz）
- データベースからランダムにクイズをひとつ選択して出題
  ```python
  cursor.execute("SELECT * FROM quiz")
  quizzes = cursor.fetchall()
  quiz = random.choice(quizzes)
  ```
- クイズがデータベースに存在しない場合は作成を促すメッセージを表示
  ```python
  if not quizzes:
    return "クイズがありません<br><a href='/create'>クイズを作成する</a>"
  ```
- ユーザーが回答を送信すると正誤判定を実施
  ```python
  correct = quiz['answer'].strip() == user_answer
  ```
- 正解・不正解に応じた結果表示（色分け表示）
- 別の問題に挑戦するリンクを提供

### 技術的な実装ポイント

#### データベース接続
- mysql.connectorを使用してMySQLに接続
- 各リクエストでコネクションを確立し、処理後にクローズする設計

#### セキュリティ対策
- SQLインジェクション対策としてprepared文を使用
  ```python
  cursor = conn.cursor(prepared=True)
  cursor.execute("INSERT INTO quiz (question, answer) VALUES (%s, %s)", (question, answer))
  ```

#### ユーザーエクスペリエンス
- 削除・保存前の確認ダイアログ
- 操作完了後のフィードバックメッセージ
- 入力バリデーション（空の問題や回答はエラー表示）

#### ルーティング設計
- RESTfulな設計を心がけ、適切なHTTPメソッド（GET/POST）を使用
- リダイレクトによるPRG（Post-Redirect-Get）パターンの実装でフォーム再送信問題を回避