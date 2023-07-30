import json

import psycopg2


class PostgresDB:
    """
    Класс для работы с БД
    """

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432',
                 table_name: str = 'repos_stats'):
        """
        Инициализирует экземпляр класса PostgresDB
        :param dbname: название БД
        :param user: пользователь
        :param password: пароль
        :param host: хост
        :param port: порт
        :param table_name: название таблицы
        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.table_name = table_name

        self._create_users_table()
        self._create_table()

    def _create_users_table(self):
        """
        Создает таблицу users в БД
        """
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255)
            """)

    def _create_table(self):
        """
        Создает таблицу в БД
        """
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            user_id INT,
            name VARCHAR(255),
            stars INT,
            forks INT,
            language VARCHAR(255),
            
            CONSTRAINT fk_{self.table_name}_users FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
            """)

    def add_user(self, user_name):
        """
        Добавляет пользователя в таблицу
        :param user_name: имя пользователя
        :return: id пользователя
        """
        with self.conn:
            self.cur.execute(
                f"INSERT INTO users (user_name) VALUES (%s)"
                f"RETURNING user_id", user_name)

            user_id = self.cur.fetchone()[0]

            return user_id

    def add_data(self, data, user_id):
        """
        Добавляет данные в таблицу
        :param user_id: id пользователя
        :param data: данные для добавления
        """
        with self.conn:
            for data_ in data:
                self.cur.execute(
                    f"INSERT INTO {self.table_name} (user_id, name, stars, forks, language) VALUES (%s, %s, %s, %s)",
                    (user_id, data_["name"], data_["stars"], data_["forks"], data_["language"]))

    def export_data_to_json(self):
        """
        Экспортирует данные из БД в файл JSON
        """
        with self.conn:
            self.cur.execute(f'SELECT * FROM {self.table_name}')
            data = self.cur.fetchall()

            data_dict = [{"id": data_[0], "name": data_[1], "stars": data_[2], "forks": data_[3], "language": data_[4]}
                         for data_ in data]

            with open(f"{self.table_name}.json", "w") as f:
                json.dump(data_dict, f, indent=4)

    def get_data(self, count=10, sort='name'):
        """
        Возвращает данные из БД
        :param count: количество результатов
        :param sort: колонка для сортировки
        :return: список словарей с данными
        """
        sort = sort.strip()

        with self.conn:
            self.cur.execute(f'SELECT * FROM {self.table_name} SORT BY {sort} LIMIT {count}')
            data = self.cur.fetchall()

            data_dict = [{"id": data_[0], "name": data_[1], "stars": data_[2], "forks": data_[3], "language": data_[4]}
                         for data_ in data]

            return data_dict
