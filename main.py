import requests
import datetime
from progress.bar import FillingSquaresBar
import json


final_answer = []
current_date = datetime.datetime.now().date()


def main():
    user_id = str(input('Your VK ID: '))
    yandex_token = str(input('Your yandex_token: '))
    mylist_vk = [0]
    bar_vk = FillingSquaresBar('Загрузка файлов с ВК', max=len(mylist_vk))
    photos_get(user_id)
    if 199 < response_vk.status_code < 300:
        bar_vk.next()
        bar_vk.finish()
        load_photos(yandex_token)
        save_information(final_answer)
    else:
        print("Ошибка, перезапустите программу.")


def photos_get(vk_id: str):
    # a function that receives photos from the VK API.
    url = 'https://api.vk.com/method/photos.get'
    # to successfully execute the function, you must enter the access_token variable in the str format
    access_token = str
    params = {
        'access_token': access_token,
        'owner_id': vk_id,
        'album_id': 'profile',
        'extended': '1',
        'photo_sizes': '1',
        'v': '5.199'
    }
    global response_vk
    response_vk = requests.post(url, params=params)


def load_photos(yandex_token):
    """
    this is a function for uploading photos to Yandex. disk,
    which first creates a request to create a folder on Yandex. disk, and then adds photos there in a request cycle
    """
    load_bar = len(response_vk.json()['response']['items']) + 1
    bar_load = FillingSquaresBar('Загрузка файлов на Я. Диск', max=load_bar)
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        'path': f'vk_backup_{current_date}'
    }
    headers = {
        'Authorization': yandex_token
    }
    requests.put(url=url, params=params, headers=headers)
    bar_load.next()
    for photo in response_vk.json()['response']['items']:
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'/vk_backup_{current_date}/{photo['likes']['count']}.jpg',
            'url': f'{photo['sizes'][-1]['url']}'
        }
        headers = {
            'Authorization': yandex_token
        }
        requests.post(url=url, params=params, headers=headers)
        final_answer.append({
            "file_name": f'{photo['likes']['count']}.jpg',
            "size": f'{photo['sizes'][-1]['type']}'
        })
        bar_load.next()

    bar_load.finish()


def save_information(final__answer):
        with open(f'vk_backup_{current_date}.json', 'w') as f:
            json.dump(final__answer, f)



main()



