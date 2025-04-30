# Алфавит по Приложению 2
alphabet = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
    'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
    'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',
    ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# Функция определения простоты
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Обратный элемент по модулю
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

# Генерация ключей
def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбираем e как наибольшее простое < p
    e = p - 1
    while not is_prime(e) or gcd(e, phi) != 1:
        e -= 1

    d = mod_inverse(e, phi)
    return (e, n), (d, n)

# Шифрование
def encrypt(pub_k, msg):
    e, n = pub_k
    crypt = []
    for char in msg:
        try:
            idx = alphabet.index(char.upper())
        except ValueError:
            print(f"Ошибка: Символ '{char}' отсутствует в алфавите.")
            continue
        encrypted = pow(idx, e, n)
        crypt.append(encrypted)
    return crypt

# Дешифрование
def decrypt(priv_k, cipher):
    d, n = priv_k
    decrypted = []
    for num in cipher:
        decoded_index = pow(num, d, n)
        if 0 <= decoded_index < len(alphabet):
            decrypted.append(alphabet[decoded_index])
        else:
            # Защита от выхода за границы алфавита
            decoded_index %= len(alphabet)
            decrypted.append(alphabet[decoded_index])
    return ''.join(decrypted)

# ================================
#           Main
# ================================

# Простые числа для варианта 13
p = 17
q = 41

# Генерация ключей
public, private = generate_key_pair(p, q)
print("Публичный ключ: ", public)
print("Приватный ключ: ", private)

# Исходное сообщение
message = "ШМЕРКО"
encrypted_msg = encrypt(public, message)
print("\nИсходное сообщение:", message)
print("Зашифрованное сообщение:", encrypted_msg)

# Расшифрование
decrypted_msg = decrypt(private, encrypted_msg)
print("Расшифрованное сообщение:", decrypted_msg)

# Расшифровка криптограммы
cryptogram = [576, 142, 639, 421, 208, 608]
decrypted_cryptogram = decrypt(private, cryptogram)
print("\nКриптограмма:", cryptogram)
print("Расшифрованное сообщение (криптограммы):", decrypted_cryptogram)