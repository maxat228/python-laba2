import os, shutil
from log_setup import log_command

# Команда cp - копирование файлов и папок
def cp(source, destination, recursive=False):
    try:
        # Преобразуем оба пути в абсолютные
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)

        # Проверяем существование источника
        if not os.path.exists(abs_source):
            error_msg = f"No such file or directory: '{source}'"
            print(f"cp: {error_msg}")
            log_command(f"cp {'-r' if recursive else ''} {source} {destination}", success=False, error_msg=error_msg)
            return

        # Если источник - папка, но не указан флаг -r, выдаем ошибку
        if os.path.isdir(abs_source) and not recursive:
            error_msg = f"'{source}' is a directory (not copied)"
            print(f"cp: {error_msg}")
            log_command(f"cp {'-r' if recursive else ''} {source} {destination}", success=False, error_msg=error_msg)
            return

        # Выполняем копирование в зависимости от типа источника
        if os.path.isdir(abs_source):
            # Рекурсивное копирование папки со всем содержимым
            shutil.copytree(abs_source, abs_dest)
        else:
            # Копирование одиночного файла
            shutil.copy2(abs_source, abs_dest)

        # Логируем успешное выполнение команды
        log_command(f"cp {'-r' if recursive else ''} {source} {destination}", success=True)

    except Exception as error:
        # Обработка непредвиденных ошибок
        error_msg = str(error)
        print(f"cp: {error_msg}")
        log_command(f"cp {'-r' if recursive else ''} {source} {destination}", success=False, error_msg=error_msg)
