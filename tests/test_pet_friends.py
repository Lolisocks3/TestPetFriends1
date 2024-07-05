from api import PetFriends
from settings import valid_email, valid_password
import pytest
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

@pytest.fixture(params=[
    ('Alex', 'cat', '3', 'Alex.jpg'),
    ('Bob', 'dog', '5', 'dog.jpg'),
    ('Charlie', 'bird', '1', 'bird.jpg')
])
def pet_data_valid(request):
    return request.param

#Негативный тест с спецсимволами и пустыми значениями
def test_add_new_pet_with_valid_data_and_photo(pet_data_valid):
    name, animal_type, age, pet_photo_path = pet_data_valid
    pet_photo = 'C:\\Users\\i_lov\\PycharmProjects\\pythonProject\\tests\\images\\Alex.jpg'
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Тест на XSS уязвимость
def test_xss_vulnerability(name="<script>alert('xss');</script>", animal_type='xss', age='xss'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

@pytest.fixture(params=[
    ('2130&@*#&$*!)*@*)&$_!+', '№cat№', '▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟ ■ □ ▢ ', 'Alex.jpg'),
    ('🔥 🎃 👻 🍬 🦇 💀 🧡 💣 💥 ♻ 🧨 🤔 ⚠ 🔎 😘 ', ' ⒆ ⒇ ⒈ ⒉ ⒊ ⒋ ⒌ ⒍', '1000000000000', 'dog.jpg'),
    ('♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ', '', '', 'bird.jpg')
])
def pet_data_unvalid(request):
    return request.param

def test_add_new_pet_with_unvalid_data_and_photo(pet_data_unvalid):
    name, animal_type, age, pet_photo_path = pet_data_unvalid
    pet_photo = 'C:\\Users\\i_lov\\PycharmProjects\\pythonProject\\tests\\images\\Alex.jpg'
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_valid_data_without_photo(name='Alex', animal_type='cat', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_delete_self_pet():
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

@pytest.mark.xfail
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

def test_delete_all_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status = None

    while my_pets['pets']:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert len(my_pets['pets']) == 0


