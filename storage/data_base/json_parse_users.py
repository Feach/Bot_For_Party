# Файл создания json файла для работы с юзерами

import requests
import json

headers ={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


def get_json(url):
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return data


def main():
    get_json(url="http://127.0.0.1:8000/users/?format=json")


if __name__ == "__main__":
    main()