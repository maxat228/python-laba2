import os, shutil
from log_setup import log_command

# Команда mv - перемещение или переименовывание файлов/папок
def mv(source, destination):
    try:
        # Преобразуем оба пути в абсолютные
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)

        # Проверяем существование источника
        if not os.path.exists(abs_source):
            error_msg = f"No such file or directory: '{source}'"
            print(f"mv: {error_msg}")
            log_command(f"mv {source} {destination}", success=False, error_msg=error_msg)
            return

        # Выполняем перемещение/переименование
        shutil.move(abs_source, abs_dest)
        # Логируем успешное выполнение команды
        log_command(f"mv {source} {destination}", success=True)

    except Exception as error:
        # Обработка непредвиденных ошибок
        error_msg = str(error)
        print(f"mv: {error_msg}")
        log_command(f"mv {source} {destination}", success=False, error_msg=error_msg)
