import os

from functions import get_repos_stats
from postgres_db import PostgresDB


params = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}


def main():
    """
    Задает основную логику программы
    """
    user_name = input("Введите имя пользователя\n")
    stat = get_repos_stats(user_name)

    db = PostgresDB(**params)
    db.add_data(stat)
    db.export_data_to_json()


if __name__ == '__main__':
    main()
