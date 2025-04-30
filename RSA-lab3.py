from math import gcd  # Импорт функции gcd из модуля math

class Handbook:
    @staticmethod
    def get_encrypt_dictionary():
        # Алфавит для шифрования
        alphabet = [
            "№", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
            "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ы", "Ъ", "Э", "Ю", "Я", " ", "0", "1", "2", "3", "4", "5", "6", "8", "9", "-",
            "_", "!", "@", "#", "+", "=", "(", ")"
        ]
        return {char: index for index, char in enumerate(alphabet)}

    @staticmethod
    def get_decrypt_dictionary():
        encrypt_dict = Handbook.get_encrypt_dictionary()
        return {v: k for k, v in encrypt_dict.items()}

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

class RSA:
    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.n = p * q
        self.e = e
        self.d = 0
        self.ENCRYPT_MAP = Handbook.get_encrypt_dictionary()
        self.DECRYPT_MAP = Handbook.get_decrypt_dictionary()
        self.create_keys()

    def show_open_key(self):
        print(f"Публичный ключ: ({self.e}, {self.n})")

    def show_close_key(self):
        print(f"Приватный ключ: ({self.d}, {self.n})")

    def encrypt(self, message):
        encrypted = []
        for char in message:
            char_num = self.ENCRYPT_MAP[char]
            var = pow(char_num, self.e, self.n)
            encrypted.append(var)
        return encrypted

    def decrypt(self, encrypted_list):
        decrypted = ""
        for num in encrypted_list:
            var = pow(num, self.d, self.n)
            decrypted += self.DECRYPT_MAP[var]
        return decrypted

    def create_keys(self):
        euler_func_value = self.euler_function(self.p, self.q)
        self.d = self.get_d(euler_func_value, self.e)

    @staticmethod
    def euler_function(p, q):
        return (p - 1) * (q - 1)

    def get_d(self, euler_func_value, e):
        d = 0
        while (d * e) % euler_func_value != 1:
            d += 1
        return d

# Пример использования
p = 17
q = 41
e = 13  # Пример значения для e, соответствующего вашему описанию
message = "ШМЕРКО"

rsa = RSA(p, q, e)  # Создание объекта RSA с параметрами p, q и e
rsa.show_open_key()  # Вывод открытого ключа
rsa.show_close_key()  # Вывод закрытого ключа
encrypted_message = rsa.encrypt(message)  # Шифрование сообщения
decrypted_message = rsa.decrypt(encrypted_message)  # Дешифрование сообщения

print(f"\nИсходное сообщение: {message}")
print(f"Зашифрованное сообщение: {encrypted_message}")
print(f"Расшифрованное сообщение: {decrypted_message}")

# Table
encrFromTable = [576, 142, 639, 421, 208, 608]
print(f"\nКриптограмма: {encrFromTable}")
decrypted_message = rsa.decrypt(encrFromTable)
print(f"Расшифрованное сообщение (криптограммы): {decrypted_message}")