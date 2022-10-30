import os
import json
import mysql.connector
import boto3


def get_mysql_host():
    """
    get_mysql_host retourne l'url de la base de données MySQL.
    :return: l'url de la base de données MySQL
    """
    # La variable d'environnement MYSQL_LOCAL_HOST est utilisée pour les développement en local avec Docker
    if os.environ.get("MYSQL_LOCAL_HOST"):
        return os.environ["MYSQL_LOCAL_HOST"]

    # On récupère l'url de la base de données RDS afin de s'y connecter pour lire et insérer des commentaires
    client = boto3.client('rds')
    instances = client.describe_db_instances(DBInstanceIdentifier=os.environ["MYSQL_DB_INSTANCE"])
    return instances.get('DBInstances')[0].get('Endpoint').get('Address')


class CommentDB:
    __connection = None

    def set_connection(self):
        """
        set_connection établit une connexion avec la base de données RDS
        et initialise la variable local __connection
        et crée la table Comments avec la fonction __create_table
        """
        if not self.__connection:
            self.__connection = mysql.connector.connect(host=get_mysql_host(),
                                                        database=os.environ["MYSQL_DATABASE"],
                                                        user=os.environ["MYSQL_USER"],
                                                        password=os.environ["MYSQL_PASSWORD"])
            self.__create_table()

    def __create_table(self):
        """
        __create_table crée la table Comments si elle n'existe pas déjà
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
                CREATE TABLE comments
                (
                    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                    name VARCHAR(100),
                    comment VARCHAR(255),
                    article_id VARCHAR(100),
                    date VARCHAR(100)
                );
            """)
            cursor.fetchone()
            print("Table created")
        except Exception as ex:
            print(ex)

    def __drop_table(self):
        """
        __drop_table supprime la table Comments
        """
        cursor = self.__connection.cursor()
        cursor.execute(f"""
            DROP TABLE comments;
        """)
        record = cursor.fetchone()
        return record

    def get_comments(self, article_id: str=None):
        """
        get_comments retourne les commentaires contenus dans la base de données MySQL
        pour un article donnée identifié avec le paramètre d'entrée article_id

        :param article_id: l'identifiant de l'article lu par le visiteur
        :return: retourne l'ensemble des commentaires filtrés
        """
        self.set_connection()
        cursor = self.__connection.cursor()
        cursor.execute("""
            SELECT JSON_ARRAYAGG(JSON_OBJECT('name', name, 'comment', comment, 'date', date))
            FROM comments;
         """)
        record = cursor.fetchone()
        result = record[0]
        if result:
            return json.loads(result)
        else:
            return []

    def insert_comment(self, name, comment, article_id, date):
        """
        insert_comment insère un commentaire dans la table Comments

        :param name: le nom du visiteur qui laisse un commentaire
        :param comment: le contenu du commentaire
        :param article_id: l'identifiant de l'article lu par le visiteur
        :param date: la date à laquelle le commentaire a été laissé
        """
        self.set_connection()
        cursor = self.__connection.cursor()
        cursor.execute(f"""
            INSERT INTO comments (name, comment, article_id, date)
            VALUES ('{name}', '{comment}', '{article_id}', '{date}');
        """)
        self.__connection.commit()
