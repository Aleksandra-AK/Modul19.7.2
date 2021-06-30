from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key, empty_email, empty_password
import os
import pytest


pf: PetFriends = PetFriends()


class Tests:

    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert status == 200

    @pytest.mark.auth
    def test_get_api_key_for_valid_user(self, get_key):
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200

    @pytest.mark.api
    def test_get_all_pets_with_valid_key(self, filter=''):
            """ Проверяем что запрос всех питомцев возвращает не пустой список.
                Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
                запрашиваем список всех питомцев и проверяем что список не пустой.
                Доступное значение параметра filter - 'my_pets' либо '' """
            self.status, result = self.pf.get_list_of_pets(self.key, filter)
            assert len(result['pets']) > 0

    @pytest.mark.ui
    @pytest.mark.event
    def test_post_add_new_pet_with_valid_data(self, name='Куропатыч', animal_type='петух',
                                              age='7', pet_photo='images/giraffe.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        self.status, result = self.pf.get_list_of_pets(self.key)

        # Добавляем питомца
        status, result = pf.add_new_pet(self.key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом  xc
        assert status == 200
        assert result['name'] == name

    @pytest.mark.api
    @pytest.mark.auth
    def test_delete_pet_correct(self):
        """Проверяем возможность удаления питомца"""
        # Получаем ключ auth_key и запрашиваем список своих питомцев
        self.status, result = self.pf.get_list_of_pets(self.key)
        _, my_pets = pf.get_list_of_pets(self.key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(self.key, "Суперкотттт", "кот", "3", "images/1174945.jpg")
            _, my_pets = pf.get_list_of_pets(self.key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(self.key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(self.key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert self.status == 200
        assert pet_id not in my_pets.values()

    @pytest.mark.ui
    @pytest.mark.event
    def test_update_pet_info_successful(self, name='Куропа', animal_type='голубь', age='5'):
        """Проверяем возможность обновления информации о питомце"""
        # Получаем ключ auth_key и список своих питомцев
        self.status, result = self.pf.get_list_of_pets(self.key)
        _, my_pets = pf.get_list_of_pets(self.key, "my_pets")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    @pytest.mark.ui
    @pytest.mark.event
    def test_create_pet_simple_without_photo_valid(self, name=45, animal_type='hgd', age='4'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        self.status, result = self.pf.get_list_of_pets(self.key)

        # Добавляем питомца
        status, result = pf.create_pet_simple_without_photo(self.key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

    @pytest.mark.ui
    @pytest.mark.event
    def test_add_photo(self, pet_photo='images/maxresdefault.jpg'):

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_default_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Получаем ключ auth_key и список своих питомцев
        self.status, result = self.pf.get_list_of_pets(self.key)
        _, my_pets = pf.get_list_of_pets(self.key, "my_pets")
        pet_id = ''
        if len(my_pets['pets']) > 0:
            for pet in my_pets['pets']:

                if pet['pet_photo'] == '':
                    status, result = pf.add_photo_of_a_pet(self.key, pet['id'], pet_photo)
                    pet_id = pet['id']

                    assert status == 200

                break
            print("No animals without photos")
        else:
            print("There is no animals")

        _, my_pets = pf.get_list_of_pets(self.key, "my_pets")

        if len(my_pets['pets']) > 0:
            for pet in my_pets['pets']:
                if pet_id == pet['id']:

                    assert pet['pet_photo'] is not ''

    @pytest.mark.api
    @pytest.mark.auth
    def test_get_api_key_for_invalid_user_email(self, email=invalid_email, password=valid_password):
        """ Проверяем что запрос api ключа возвращает статус 403 при использовании неверного email"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        self.status, result = self.pf.get_list_of_pets(self.key)

        # Сверяем полученные данные с нашими ожиданиями
        assert self.status == 403
        print('Email incorrect')

    @pytest.mark.api
    @pytest.mark.auth
    @pytest.mark.skip(reason="Для переноса в другую папку тестов")
    def test_get_api_key_for_invalid_user_password(email=valid_email, password=invalid_password):
        """ Проверяем что запрос api ключа возвращает статус 403 при использовании неверного password"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        print('Password incorrect')

    @pytest.mark.skip(reason="негативный тест, надо перенести в отдельную папку")
    def test_get_all_pets_with_invalid_key(filter=''):
        """ Проверяем что запрос всех питомцев статус ошибки 403 при неверных данных ключа.
            Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
            запрашиваем список всех питомцев и проверяем что список не пустой.
            Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = pf.get_list_of_pets(invalid_auth_key, filter)

        assert status == 403
        print('Provided auth_key is incorrect')

    @pytest.mark.xfail(reason="Нет обработки ошибки имени")
    def test_post_add_new_pet_with_invalid_data_name(self, name='', animal_type='Spider',
                                                     age='0', pet_photo='images/1235980.jpg'):
        """Проверяем что нельзя добавить питомца с некорректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        self.status, result = self.pf.get_list_of_pets(self.key)

        # Добавляем питомца
        status, result = pf.add_new_pet(self.key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        print('Provided data is incorrect')
    # Данный тест будет провален, так как поему-то можно создать питомца без имени,
    # но судя по апи, имя должно быть обязательным.

    @pytest.mark.xfail(reason="При вводе неверных данных нет ошибок")
    def test_post_add_new_pet_with_png_photo_file(self, name='Мурзик', animal_type='Кот',
                                                     age='3', pet_photo='images/british.png'):
        """Проверяем что нельзя добавить питомца с некорректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        self.status, result = self.pf.get_list_of_pets(self.key)

        # Добавляем питомца
        status, result = pf.add_new_pet(self.key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        print('Provided data is incorrect')

    @pytest.mark.skip(reason="Для переноса в другую папку тестов")
    def test_get_api_key_for_empty_user(email=empty_email, password=empty_password):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'key' in result
