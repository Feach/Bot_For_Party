# Модуль с функциями для получения json data для последующей работой с ней

import requests
from config import PARSE_PARTY_LIST_URL

from config import headers


def get_json(url):
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return data


def main():
    get_json(url=PARSE_PARTY_LIST_URL)


if __name__ == "__main__":
    main()


