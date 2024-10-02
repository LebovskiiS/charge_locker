import random

def create_cookies():
    # Генерация 10 случайных символов ASCII
    random_chars = [chr(random.randint(0, 127)) for _ in range(10)]
    random_string = ''.join(random_chars)
    payload = hex(hash(random_string))
    return payload


