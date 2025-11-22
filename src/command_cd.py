import os
from log_setup import log_command

# Команда cd - смена текущей рабочей директории
def cd(path):
    try:
        # Обработка специальных случаев
        if path == "..":
            # Переход на уровень выше - получаем родительскую директорию
            new_path = os.path.dirname(os.getcwd())
        elif path == "~":
            # Переход в домашнюю директорию пользователя
            new_path = os.path.expanduser("~")
        else:
            # Обычный путь преобразуем в абсолютный
            new_path = os.path.abspath(path)

        if not os.path.exists(new_path):
            error_msg = f"No such file or directory: '{path}'"
            print(f"cd: {error_msg}")
            log_command(f"cd {path}", success=False, error_msg=error_msg)
            return

        if not os.path.isdir(new_path):
            error_msg = f"'{path}' is not a directory"
            print(f"cd: {error_msg}")
            log_command(f"cd {path}", success=False, error_msg=error_msg)
            return

        os.chdir(new_path)
        log_command(f"cd {path}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"cd: {error_msg}")
        log_command(f"cd {path}", success=False, error_msg=error_msg)
