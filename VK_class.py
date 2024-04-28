import requests

class VK_person:
    def __init__(self, id: str):
        self.id = id


    def photos_get(self):
        # a function that receives photos from the VK API.
        url = 'https://api.vk.com/method/photos.get'
        # to successfully execute the function, you must enter the access_token variable in the str format
        access_token = str
        params = {
            'access_token': access_token,
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'v': '5.199'
        }
        response_vk = requests.post(url, params=params)
        return response_vk