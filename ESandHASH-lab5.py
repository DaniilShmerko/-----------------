import struct

class MD4:
    width = 32
    mask = 0xFFFFFFFF
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

    def __init__(self, msg=None):
        if msg is None:
            msg = b""

        self.msg = msg
        ml = len(msg) * 8
        msg += b"\x80"
        msg += b"\x00" * (-(len(msg) + 8) % 64)
        msg += struct.pack("<Q", ml)

        self._process([msg[i: i + 64] for i in range(0, len(msg), 64)])

    def __repr__(self):
        if self.msg:
            return f"{self.__class__.__name__}({self.msg})"
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.hexdigest()

    def __eq__(self, other):
        return self.h == other.h

    def bytes(self):
        return struct.pack("<4L", *self.h)

    def hexbytes(self):
        return self.hexdigest().encode()

    def hexdigest(self):
        return "".join(f"{value:02x}" for value in self.bytes())

    def _process(self, chunks):
        for chunk in chunks:
            X, h = list(struct.unpack("<16I", chunk)), self.h.copy()

            # R 1.
            Xi = [3, 7, 11, 19]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n, Xi[n % 4]
                hn = h[i] + MD4.F(h[j], h[k], h[l]) + X[K]
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # R 2.
            Xi = [3, 5, 9, 13]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n % 4 * 4 + n // 4, Xi[n % 4]
                hn = h[i] + MD4.G(h[j], h[k], h[l]) + X[K] + 0x5A827999
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # R 3.
            Xi = [3, 9, 11, 15]
            Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = Ki[n], Xi[n % 4]
                hn = h[i] + MD4.H(h[j], h[k], h[l]) + X[K] + 0x6ED9EBA1
                h[i] = MD4.lrot(hn & MD4.mask, S)

            self.h = [((v + n) & MD4.mask) for v, n in zip(self.h, h)]

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def lrot(value, n):
        lbits, rbits = (value << n) & MD4.mask, value >> (MD4.width - n)
        return lbits | rbits

def verify_signature(message, signature, public_key):
    n, e = public_key
    decrypted_signature = pow(signature, e, n)
    return decrypted_signature == message

def main():
    print("Запуск MD4.\n")

    # Проверка MD4 для пустой строки
    messages = [b""]
    known_hashes = ["31d6cfe0d16ae931b73c59d7e0c089c0"]

    for message, expected in zip(messages, known_hashes):
        result = MD4(message).hexdigest()
        print("Message: ", message)
        print("Ожидание:", expected)
        print("Получилось: ", result)
        print("Проверка результата:", result == expected)
        print()

    # Вычисление MD4 для заданных hex-чисел
    hex_strings = [
        "839c7a4d7a92cb5678a5d5b9eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edd45e51fe39708bf9427e9c3e8b9",
        "839c7a4d7a92cbd678a5d529eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edc45e51fe39708bf9427e9c3e8b9",
    ]
    hashes = []
    for hex_string in hex_strings:
        message = bytes.fromhex(hex_string)
        md4_hash = MD4(message).hexdigest()
        hashes.append(md4_hash)
        print(f"MD4({hex_string}) = {md4_hash}")

    print("\nПроверка, что хэши разные:", hashes[0] != hashes[1])

    # Проверка цифровой подписи
    print("\nПроверка цифровой подписи:")
    public_key = (55, 3)
    messages = [(7, 28), (288, 15), (16, 36)]

    for message, signature in messages:
        is_valid = verify_signature(message, signature, public_key)
        if is_valid:
            print(f"Подпись для сообщения {message} верна.")
        else:
            print(f"Подпись для сообщения {message} недействительна.")

if __name__ == "__main__":
    main()