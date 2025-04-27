import random

# Алгоритм "Решето Эратосфена"
def sieve_of_eratosthenes(n):
    # Инициализация списка чисел со значением True для выявления простых чисел
    primes = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        # Если primes[p] не изменен, значит p простое
        if primes[p] == True:
            # Обновление всех кратных p
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    # Инициализация финального списка, заполненным простыми числами (True)
    prime_numbers = [p for p in range(2, n + 1) if primes[p]]
    return prime_numbers

# Тест Миллера-Рабина
def miller_rabin(m, r):
    # Представить m - 1 в виде 2^s * t
    t = m - 1
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1
    for _ in range(r):  # Цикл А
        a = random.randint(2, m - 2)
        x = pow(a, t, m)
        if x == 1 or x == m - 1:
            continue

        for _ in range(s - 1):  # Цикл B
            x = pow(x, 2, m)  # x = x^2 % m
            if x == m - 1:
                break
            if x == 1:
                return "составное"
        else:
            return "составное"

    return "вероятно простое"

# Нахождение первообразных корней
def find_primitive_root(p):
    # Нахождение всех делителей p-1
    divisors = []
    for i in range(2, int((p - 1) ** 0.5) + 1):
        if (p - 1) % i == 0:  # Если число делит нацело p−1, оно добавляется в список делителе
            divisors.append(i)
            if i != (p - 1) // i:  # добавляется частное от деления p−1 на делитель, если оно отличается от самого делителя.
                divisors.append((p - 1) // i)
    # Проверка каждого числа g от 2 до p-1
    result = []
    for g in range(2, p):
        valid = True
        for d in divisors:
            if pow(g, d, p) == 1:
                valid = False
                break
        if valid:
            result.append(g)
    return result

def transfer(q, a):
    # Секретное число каждого абонента
    Xa = random.randint(0, q)
    Xb = random.randint(0, q)
    # Открытое значение каждого абонента
    Ya = pow(a, Xa, q)
    Yb = pow(a, Xb, q)
    # Вычисление общего ключа
    Ka = pow(Yb, Xa, q)
    Kb = pow(Ya, Xb, q)
    if Ka == Kb:
        return Ka
    else:
        return "Ключ вычислить не удалось"

# Получаем все простые числа
n = 100
primes = sieve_of_eratosthenes(n)
print("Простые числа:\n", primes)

# Проверяем одно из полученных чисел, и удостоверяемся, что оно не составное
m = 71  # Число для проверки
r = 6  # Количество раундов
result = miller_rabin(m, r)
print(f"\nЧисло {m}", result)

# Находим первообразные корни по модулю простого числа
p = find_primitive_root(m)
print(f"\nПервообразные корни числа {m}:\n", p)

# Выполнение обмена ключами
q = m
a = random.choice(p)
K = transfer(q, a)
print("\nВычисленный секретный ключ:", K)