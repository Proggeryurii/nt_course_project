import datetime
from progress.bar import FillingSquaresBar
import json
from VK_class import VK_person
from Yandex_disk_class import Yandex_disk


def main():
    user_id = str(input('Your VK ID: '))
    yandex_token = str(input('Your yandex_token: '))
    vk_person = VK_person(user_id)
    mylist_vk = [1]
    bar_vk = FillingSquaresBar('Загрузка файлов с ВК', max=len(mylist_vk))
    response_vk = vk_person.photos_get()
    status = response_vk.status_code
    if 199 < status < 300:
        bar_vk.next()
        bar_vk.finish()
        yd_person = Yandex_disk(yandex_token)
        status_yd = yd_person.load_photos(response_vk.json())
        if status_yd != '1':
            save_information(status_yd)
        else:
            print("Ошибка")
            return 1
    else:
        print("Ошибка, перезапустите программу.")


def save_information(final__answer):
    current_date = datetime.datetime.now().date()
    with open(f'vk_backup_{current_date}.json', 'w') as f:
        json.dump(final__answer, f)


if __name__ == "__main__":
    main()



