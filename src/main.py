from functions import get_repos_stats
from postgres_db import PostgresDB
from config import config


def main():
    """
    Задает основную логику программы
    """
    # получаем параметры для подключения к БД из файла
    params = config()

    # получаем имя пользователя и статистику его репозиториев
    user_name = input("Введите имя пользователя\n").strip()
    stat = get_repos_stats(user_name)

    # подключаемся к БД
    db = PostgresDB(**params)

    # добавляем пользователя и статистику его репозиториев
    user_id = db.add_user(user_name)
    db.add_data(stat, user_id)

    # экспортируем данные в JSON файл
    db.export_data_to_json()


if __name__ == '__main__':
    main()
