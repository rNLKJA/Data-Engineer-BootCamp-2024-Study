import sys
import time
import json
import requests

def create_server_connection():
    session_url = 'http://localhost:80/api/login'
    server_url = 'http://localhost:80/api/servers/'

    login_data = {
        'email': 'admin@admin.com',
        'password': 'root'
    }

    server_data = {
        'Servers': {
            '1': {
                'name': 'Docker localhost',
                'host': 'pg-database',
                'port': 5432,
                'username': 'root',
                'password': 'root',
                'db': 'postgres',
                'sslmode': 'prefer'
            }
        }
    }

    session = requests.Session()
    session.post(session_url, json=login_data)

    session.post(server_url, json=server_data)

if __name__ == '__main__':
    time.sleep(10)
    create_server_connection()
