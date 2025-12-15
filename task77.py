import requests
import re

class MyFile:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode.lower()
        valid_modes = ('read', 'write', 'append', 'url')
        if self.mode not in valid_modes:
            raise ValueError(f"Неверный режим! Используйте один из {valid_modes}")

    def checkread(self):
        if self.mode != 'read':
            raise ValueError("Неверный режим! Используйте режим 'read'")

    def checkwrite(self):
        if self.mode not in ('write', 'append'):
            raise ValueError("Неверный режим! Используйте режим 'write' или 'append'")

    def checkurl(self):
        if self.mode != 'url':
            raise ValueError("Неверный режим! Используйте режим 'url'")

    def read(self):
        self.checkread()
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")
        except Exception as e:
            raise IOError(f"Ошибка при чтении файла: {e}")

    def write(self, text):
        self.checkwrite()
        mode = 'w' if self.mode == 'write' else 'a'
        try:
            with open(self.path, mode, encoding='utf-8') as f:
                f.write(text + '\n')
        except Exception as e:
            raise IOError(f"Ошибка при записи в файл: {e}")

    def getp(self):
        self.checkurl()
        try:
            response = requests.get(self.path)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при доступе к URL '{self.path}': {e}")

    def readurl(self):
        return self.getp()

    def countur(self):
        txt = self.getp()
        return len(re.findall(r'https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]+', txt))

    def writeurl(self, filepath):
        htmltype = self.getp()
        try:
            #mode = 'a' if os.path.exists(filepath) else 'w'
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(htmltype)
        except Exception as e:
            raise IOError(f"Ошибка при записи URL в файл: {e}")


#Проверка работа способности класса:

file = MyFile("test.txt", "read")
text = file.read() # происходит чтение в виде str
print(text)

file = MyFile("test.txt", "write")
text = file.write("привет! 1") # происходит запись строки в файл

file = MyFile("test.txt", "append")
text = file.write("привет! 2") # происходит добавление строки в конец файла

# указали URL
file = MyFile("https://dfedorov.spb.ru/", "url")
# и может читать содержимое страницы по указанному URL
text = file.readurl() # происходит чтение в виде str
print(text)

# возвращает кол-во url адресов на странице, например, методом count
count = file.countur()
print('Количество url адресов на странице:', count)

# происходит запись содержимого страницы по URL в указанный файл
file.writeurl("test-url.txt")
