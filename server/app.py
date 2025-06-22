#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Clear session
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Get all articles
@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles]), 200

# Get single article with paywall logic
@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views in session if not set
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if article:
            return jsonify(article.to_dict()), 200
        else:
            return {'message': 'Article not found'}, 404
    else:
        return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5555)
