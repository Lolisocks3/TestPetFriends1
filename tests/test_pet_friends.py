from api import PetFriends
from settings import valid_email, valid_password
import os
import requests
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data_and_photo(name='Alex', animal_type='cat',
                                     age='3', pet_photo='images/Alex.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_valid_data_without_photo(name='Alex', animal_type='cat', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Alex", "cat", "3", "images/Alex.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Alex', animal_type='cat', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        print("Нет питомцев в моём списке")

def test_load_photo_of_pet(pet_photo='images/NotAlex.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, "Alex", "cat", "3")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert my_pets['pets'][0]['name'] == "Alex"
    pet_id = my_pets['pets'][0]['id']
    with open(pet_photo, 'rb') as f:
        pet_photo_data = f.read()
    status, result = pf.load_photo_of_pet(auth_key, pet_id, pet_photo_data)
    assert status == 200
    _, pet_info = pf.get_pet_info(auth_key, pet_id)
    assert pet_info['pet_photo'] == f'images/pets/{pet_id}.jpg'




