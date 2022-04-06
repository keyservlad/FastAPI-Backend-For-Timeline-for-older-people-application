
# ## MySQL credentials

# DB_NAME_SQL : sherbrooke_ift785_annotations
# HOST_SQL: mysql-sherbrooke.alwaysdata.net
# PORT_SQL : 3306
# USERNAME_SQL : 262938
# PASSWORD_SQL : Sr25qzz4@nf36mB

import string
import psycopg2
import mysql.connector

class Database()

class MySQL:
    def __init__(self, host: str, port: str, database: str, username:str, password:str):
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        self.connexion = mydb
        print('Connexion succeeded')
        print(self.connexion)


class PostgreSQL:
    def __init__(self, host: str, port: str, database: str, username:str, password:str):
        conn = psycopg2.connect(
            host=host,
            database=database,
            port=port,
            user=username,
            password=password
        )
        self.connexion = conn
        print('Connexion succeeded')
        print(self.connexion)



if __name__ == '__main__':
    
    case = 'remote'

    if case == 'local':
        postgresql = PostgreSQL(
            'localhost', 
            '5432', 
            'ift785', 
            'postgres', 
            'admin'
        )
        _mysql = MySQL(
            'localhost', 
            '3306', 
            'ift785',
            'mysql',
            'admin'
        )
    elif case == 'remote':
        postgresql = PostgreSQL(
            'postgresql-sherbrooke.alwaysdata.net',
            '5432', 
            'sherbrooke_ift785_annotations', 
            'sherbrooke',
            'Sr25qzz4nf36mB'
        )
        _mysql = MySQL(
            'mysql-ift785-pene.alwaysdata.net', 
            '3306', 
            'ift785-pene_mysql',
            '263455',
            'PxN9GvaUZAfBR!z'
        )
