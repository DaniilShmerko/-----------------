from math import gcd

# Алфавит для шифрования
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Функция для получения индекса символа в алфавите
def char_to_num(char):
    return ALPHABET.index(char) + 1

# Функция для получения символа по его индексу
def num_to_char(num):
    return ALPHABET[num - 1]

# Функция для нахождения модульного обратного
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
def is_prime(num):
    """Проверка числа на простоту."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    """Нахождение наибольшего общего делителя."""
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Нахождение обратного элемента d по модулю phi."""
    k = 1
    while (k * phi + 1) % e != 0:
        k += 1
    return (k * phi + 1) // e

# Класс для реализации RSA
class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.find_e()
        self.d = mod_inverse(self.e, self.phi)

    def find_e(self):
        """Нахождение открытой экспоненты e."""
        for e in range(2, self.phi):
            if gcd(e, self.phi) == 1:
                return e
        raise ValueError("Не удалось найти подходящее значение e.")

    def encrypt(self, message):
        """Шифрование сообщения."""
        encrypted = []
        for char in message:
            char_num = ord(char)  # Преобразуем символ в его ASCII-код
            encrypted_char = pow(char_num, self.e, self.n)
            encrypted.append(encrypted_char)
        return encrypted

    def decrypt(self, encrypted_message):
        """Дешифрование сообщения."""
        decrypted = ""
        for num in encrypted_message:
            decrypted_char = pow(num, self.d, self.n)
            decrypted += chr(decrypted_char)  # Преобразуем ASCII-код обратно в символ
        return decrypted

# Основная часть программы
if __name__ == "__main__":
    # Исходные данные
    p = 17
    q = 41
    message = "Шмерко"
    cryptogram = [576, 142, 639, 421, 208, 608]

    # Создание объекта RSA
    rsa = RSA(p, q)

    # Вывод ключей
    print(f"Открытый ключ: (e, n) = ({rsa.e}, {rsa.n})")
    print(f"Закрытый ключ: (d, n) = ({rsa.d}, {rsa.n})")

    # Шифрование сообщения
    encrypted_message = rsa.encrypt(message)
    print(f"Исходное сообщение: {message}")
    print(f"Зашифрованное сообщение: {encrypted_message}")

    # Дешифрование криптограммы
    decrypted_message = rsa.decrypt(cryptogram)
    print(f"Криптограмма: {cryptogram}")
    print(f"Расшифрованное сообщение: {decrypted_message}")