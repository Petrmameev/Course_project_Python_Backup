import requests

import setting
from time import sleep
from tqdm import tqdm


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def json_data(self):

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': album_id,
                  'count': 6,
                  'rev': 1,
                  'extended': 1,
                  'photo_sizes': 1
                  }
        response = requests.get(url, params={**self.params, **params})
        data = response.json()
        return data

    def photos(self):
        dict_max_size_foto = {}
        data = self.json_data()
        list_foto = data['response']['items']
        for foto in list_foto:
            file_name = foto['likes']['count']
            file_name_if_have = f'{foto["likes"]["count"]}{foto["date"]}'
            size_dict = {'s': 0, 'm': 1, 'o': 2, 'p': 3, 'q': 4, 'r': 5, 'x': 6, 'y': 7, 'z': 8, 'w': 9}
            max_size_foto = max(foto['sizes'], key=lambda x: size_dict[x['type']])
            if file_name not in dict_max_size_foto.keys():
                dict_max_size_foto[file_name] = {max_size_foto['type']: max_size_foto['url']}
            else:
                dict_max_size_foto[file_name_if_have] = {max_size_foto['type']: max_size_foto['url']}
        return (dict_max_size_foto)


access_token = setting.TOKEN_VK
user_id = input('Введите id пользователя VK: ')

vk = VK(access_token, user_id)


# print(vk.photos())


class YaUploader:
    name_folder = 'Foto VK1'

    def __init__(self, access_token_yandex: str):
        self.token = access_token_yandex
        self.HOST = 'https://cloud-api.yandex.net/'

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self):
        uri = 'v1/disk/resources'
        url = self.HOST + uri
        params = {'path': self.name_folder, 'overwrite': 'true'}
        response = requests.put(url, headers=self.get_headers(), params=params)
        return (response.json())

    def upload_foto(self):
        info_foto_in_jason = []
        uri = 'v1/disk/resources/upload'
        url = self.HOST + uri
        self.vk_fotos = VK(access_token, user_id)
        all_foto = self.vk_fotos.photos()
        self.create_folder()
        for k, v in tqdm(all_foto.items()):
            sleep(0.1)
            path_to_file = f'{self.name_folder}/{k}.jpeg'
            resp = requests.post(url, headers=self.get_headers(), params={'path': path_to_file, 'url': v.values()})
            for key_ in v.keys():
                json_foto = {"file_name": f'{k}.jpg', "size": f'{key_}'}
                info_foto_in_jason.append(json_foto)
        return (info_foto_in_jason)


album = input("""Введите "1" если хотите скачать фотографии со стены; \nВведите "2" если хотите скачать фотографии профиля;
        """)
if album == '1':
    album_id = 'wall'
elif album == '2':
    album_id = 'profile'
else:
    print('Такого альбома нет, выберите "1" или "2"')

access_token_yandex = setting.TOKEN_YA
YAN = YaUploader(access_token_yandex)
print(YAN.upload_foto())
