import os

directories = [
    'models',
    'services',
    'utils'
]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Створено директорію: {directory}")

for directory in directories:
    init_file = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""Пакет {}"""'.format(directory))
        print(f"Створено файл: {init_file}")

print("Структура проекту успішно створена.")