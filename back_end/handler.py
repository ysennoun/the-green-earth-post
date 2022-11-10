import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import CommentDB


app = Flask(__name__)
CORS(app)
comment_db = CommentDB()


@app.route('/api/health')
def health():
    """
    health permet de tester si le serveur web est bien fonctionnel
    :return: retourne une phrase
    """
    if request.args.get('showLocalIp') == 'yes':
        return f'API Server is healthy ! Local IP responding: {socket.gethostbyname(socket.gethostname())}'
    return 'API Server is healthy !'


@app.route('/api/comments', methods=['GET'])
def get_comments():
    """
    get_comments retourne tous les commentaires
    :return: retourne tous les comentaires
    """
    return comment_db.get_comments()


@app.route('/api/comment', methods=['POST'])
def post_comment():
    """
    post_comment insérer un commentaire
    """
    data = request.json
    comment_db.insert_comment(
        name=data["name"],
        comment=data["message"],
        date=data["date"]
    )
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
