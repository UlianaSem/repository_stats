import requests


def get_repos_stats(user):
    """Собирает статистику по репозиториям пользователя
    :param user: имя пользователя
    :return: список словарей со статистикой
    """
    stat_answer = []

    user_url = f'https://api.github.com/users/{user}/repos'
    params = {'per_page': 100}

    user_response = requests.get(user_url, params=params).json()

    for repo in user_response:
        stat_answer.append({
            'name': repo['name'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'language': repo['language']
        })

    return stat_answer
