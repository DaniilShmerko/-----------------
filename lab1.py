class DoublePermutationAlgorithm:
    def encrypt(self, source_text, row_key, column_key):
        table_side = len(row_key)
        table = self.create_table(source_text, table_side)
        # Перестановка строк
        table = [table[i] for i in row_key]
        # Перестановка столбцов
        table = [[row[i] for i in column_key] for row in table]
        return ''.join(''.join(row) for row in table)

    def decrypt(self, encrypted_text, row_key, column_key):
        table_side = len(row_key)
        table = [list(encrypted_text[i:i + table_side]) for i in range(0, len(encrypted_text), table_side)]
        # Обратная перестановка столбцов
        inverse_column_key = sorted(range(len(column_key)), key=column_key.__getitem__)
        table = [[row[i] for i in inverse_column_key] for row in table]
        # Обратная перестановка строк
        inverse_row_key = sorted(range(len(row_key)), key=row_key.__getitem__)
        table = [table[i] for i in inverse_row_key]
        return ''.join(''.join(row) for row in table)

    def create_table(self, source_text, side):
        table = [['?' for _ in range(side)] for _ in range(side)]
        source_text = source_text.replace(" ", "?")
        char_index = 0
        for i in range(side):
            for j in range(side):
                if char_index < len(source_text):
                    table[i][j] = source_text[char_index]
                    char_index += 1
        return table

# Пример использования
algorithm = DoublePermutationAlgorithm()

# Ключи для перестановки строк и столбцов
row_key = [5, 2, 0, 4, 3, 1]  # Пример ключа для строк
column_key = [3, 0, 1, 2, 5, 4]  # Пример ключа для столбцов

source_text = "Неясное становится еще более непонятным"
encrypted_text = algorithm.encrypt(source_text, row_key, column_key)
print("Зашифрованное сообщение:", encrypted_text)

decrypted_text = algorithm.decrypt(encrypted_text, row_key, column_key)
print("Дешифрованное сообщение:", decrypted_text.replace("?", " "), "ным")