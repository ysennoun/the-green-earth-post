from flask import Flask, request, jsonify
from flask_cors import CORS
from db import CommentDB


app = Flask(__name__)
CORS(app)
comment_db = CommentDB()


@app.route('/health')
def health():
    """
    health permet de tester si le serveur web est bien fonctionnel
    :return: retourne une phrase
    """
    return 'Web Server is healthy !'


@app.route('/comments', methods=['GET'])
def get_comments():
    """
    get_comments retourne les commentaires contenus dans la base de données MySQL
    :return: retourne l'ensemble des commentaires filtrés
    """
    return comment_db.get_comments()


@app.route('/comment', methods=['POST'])
def post_comment():
    """
    post_comment insère un commentaire dans la table Comments
    """
    data = request.json
    comment_db.insert_comment(
        name=data["name"],
        comment=data["message"],
        article_id="article_id",
        date=data["date"]
    )
    return jsonify(data)
