import requests
import datetime
from progress.bar import FillingSquaresBar


current_date = datetime.datetime.now().date()
class Yandex_disk:
    def __init__(self, yandex_token):
        self.yandex_token = yandex_token

    def load_photos(self, response_vk_json):
        """
        this is a function for uploading photos to Yandex. disk,
        which first creates a request to create a folder on Yandex. disk, and then adds photos there in a request cycle
        """
        load_bar = len(response_vk_json['response']['items']) + 1
        bar_load = FillingSquaresBar('Загрузка файлов на Я. Диск', max=load_bar)
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        name_papka = str(input("Выберете название папки для сохранения (по умолч. нажм. enter): "))
        if len(name_papka) == 0:
            name_papka = f'vk_backup_{current_date}'
        params = {
            'path': name_papka
        }
        headers = {
            'Authorization': self.yandex_token
        }
        response_papka = requests.put(url=url, params=params, headers=headers)
        if 199 < response_papka.status_code < 300:
            bar_load.next()
            final_answer = []
            for photo in response_vk_json['response']['items']:
                url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                params = {
                    'path': f'/{name_papka}/{photo["likes"]["count"]}.jpg',
                    'url': f'{photo["sizes"][-1]["url"]}'
                }
                headers = {
                    'Authorization': self.yandex_token
                }
                response = requests.post(url=url, params=params, headers=headers)
                if  199 < response.status_code < 300:
                    final_answer.append({
                        "file_name": f'{photo["likes"]["count"]}.jpg',
                        "size": f'{photo["sizes"][-1]["type"]}'
                    })
                    bar_load.next()
                else:
                    print("Ошибка, перезапустите программу.")
                    return '1'

            bar_load.finish()
        else:
            print("Ошибка, перезапустите программу.")
            return '1'
        return final_answer