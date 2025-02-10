from faker import Faker
from qrcode import QRCode, constants

def get_random_person():
    # Создаём объект Faker с русской локализацией
    fake = Faker('ru_RU')

    # Генерируем случайные данные пользователя
    user = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake. email(),
        'phone_number': fake.phone_number(),
        'birth_date': fake.date_of_birth(),
        'company': fake.company(),
        'job': fake.job()
    }
    return user

def gen_qrcode(value: str):
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black", back_color="white")
    # img.save(f'utils/f{value}.jpeg')
    return img

