import os
from log_setup import log_command

# Команда cat - вывод содержимого файла в консоль
def cat(file_path):
    try:
        # Преобразуем путь в абсолютный
        abs_file_path = os.path.abspath(file_path)

        # Проверяем существование файла
        if not os.path.exists(abs_file_path):
            error_msg = f"No such file or directory: '{file_path}'"
            print(f"cat: {error_msg}")
            log_command(f"cat {file_path}", success=False, error_msg=error_msg)
            return

        # Проверяем, что это файл, а не директория
        if os.path.isdir(abs_file_path):
            error_msg = f"'{file_path}' is a directory"
            print(f"cat: {error_msg}")
            log_command(f"cat {file_path}", success=False, error_msg=error_msg)
            return

        # Открываем файл в режиме чтения и выводим содержимое в консоль
        with open(abs_file_path, "r", encoding="utf-8") as file:
            print(file.read())

        # Логируем успешное выполнение команды
        log_command(f"cat {file_path}", success=True)

    except Exception as error:
        # Обработка непредвиденных ошибок
        error_msg = str(error)
        print(f"cat: {error_msg}")
        log_command(f"cat {file_path}", success=False, error_msg=error_msg)
