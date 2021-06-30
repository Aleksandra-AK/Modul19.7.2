import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests


def log_wrapper(func):
    def log_func(self, *args):
        res = func(self, *args)
        with open('log.txt', 'a', encoding='utf8') as log_file:
            log_file.write(f'{func.__name__}, {res[1].keys()}')
            log_file.write(f'{len(args)} headers: {args[0:]}, path parametrs: {args[2:]}')
            log_file.write(f'string parametrs: {args}, body: {args}######')
            log_file.write(f'######response: [arg5], response body: [arg6]\n')
        return res
    return log_func


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    @log_wrapper
    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
               JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @log_wrapper
    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
                со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
                либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
                собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
    @log_wrapper
    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
               запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder({
             'name': name,
             'animal_type': animal_type,
             'age': age,
             'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер запрос на обновление информации по питомцу по указанному ID
        и возвращает статус запроса на сервер и результат в формате JSON с данными измененного питомца"""

        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
           }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple_without_photo(self, auth_key: json, name: str, animal_type: str,
                                        age: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без картинки и возвращает статус
               запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_photo_of_a_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер запрос на добавление фото питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном добавлении."""

        data = MultipartEncoder({'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
