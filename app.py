from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# 投稿モデルの定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 投稿ID（主キー）
    title = db.Column(db.String(30), nullable=False)  # タイトル（必須）
    body = db.Column(db.String(300), nullable=False)  # 本文（必須）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))  # 作成日時（日本時間）

# トップページ：投稿一覧の表示
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template("index.html", posts=posts)

# 投稿作成ページ
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()  # 変更をDBに反映
        return redirect('/')
    else:
        return render_template("create.html")

# 投稿編集ページ
@app.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        db.session.commit()  # 変更をDBに反映
        return redirect('/')

# 投稿削除処理
@app.route("/<int:id>/delete", methods=['GET'])
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()  # 削除をDBに反映
    return redirect('/')

# アプリ起動 & 初回DB作成
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 初回のみ実行してDBを作成
    app.run(debug=True)
