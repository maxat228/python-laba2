import os, stat, time
from log_setup import log_command

# Команда ls - отображение файлов и каталогов
def ls(path=None, detailed=False):
    try:
        # Если путь не указан, используем текущую директорию
        if path is None:
            target_path = '.'  # Текущая директория
        else:
            target_path = path

        # Преобразуем путь в абсолютный путь
        abs_path = os.path.abspath(target_path)

        # Проверяем существует ли указанный путь
        if not os.path.exists(abs_path):
            error_msg = f"No such file or directory: '{path}'"
            print(f"ls: {error_msg}")
            # Логируем неудачную команду
            log_command(f"ls {'-l' if detailed else ''} {path}", success=False, error_msg=error_msg)
            return

        # Проверяем, что путь ведет к директории, а не к файлу
        if not os.path.isdir(abs_path):
            error_msg = f"'{path}' is not a directory"
            print(f"ls: {error_msg}")
            log_command(f"ls {'-l' if detailed else ''} {path}", success=False, error_msg=error_msg)
            return

        # Получаем список всех файлов и папок в указанной директории
        items = os.listdir(abs_path)

        # Если запрошен подробный вывод (флаг -l)
        if detailed:
            # Проходим по всем отсортированным элементам
            for element in sorted(items):
                # Полный путь к элементу
                item_path = os.path.join(abs_path, element)
                try:
                    # Получаем информацию о файле/папке (размер, права, время и прочее)
                    stat_info = os.stat(item_path)

                    # Определяем тип элемента: папка, файл или ссылка
                    if stat.S_ISDIR(stat_info.st_mode):
                        file_type = "d"  # папка
                    elif stat.S_ISLNK(stat_info.st_mode):
                        file_type = "l"  # ссылка
                    else:
                        file_type = "-"  # обычный файл

                    # Формируем строку прав доступа (rwx)
                    perm = ''
                    # Права владельца (user)
                    perm += 'r' if stat_info.st_mode & stat.S_IRUSR else '-'
                    perm += 'w' if stat_info.st_mode & stat.S_IWUSR else '-'
                    perm += 'x' if stat_info.st_mode & stat.S_IXUSR else '-'
                    # Права группы (group)
                    perm += 'r' if stat_info.st_mode & stat.S_IRGRP else '-'
                    perm += 'w' if stat_info.st_mode & stat.S_IWGRP else '-'
                    perm += 'x' if stat_info.st_mode & stat.S_IXGRP else '-'
                    # Права остальных (other)
                    perm += 'r' if stat_info.st_mode & stat.S_IROTH else '-'
                    perm += 'w' if stat_info.st_mode & stat.S_IWOTH else '-'
                    perm += 'x' if stat_info.st_mode & stat.S_IXOTH else '-'

                    # Размер файла в байтах
                    size = stat_info.st_size
                    # Преобразуем время изменения в читаемый формат
                    modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime))

                    # Выводим отформатированную информацию
                    print(f"{file_type}{perm} {size:>8} {modified_time} {element}")

                except OSError:
                    # Если не удалось получить информацию об элементе
                    print(f"?????????? ?         ????-??-?? ??:?? {element}")
        else:
            # Простой вывод с именами файлов и папок
            for element in sorted(items):
                item_path = os.path.join(abs_path, element)
                # Для папок добавляем / в конце
                if os.path.isdir(item_path):
                    print(f"{element}/")
                else:
                    print(f"{element}")

        # Логируем успешное выполнение команды
        log_command(f"ls {'-l' if detailed else ''} {path}", success=True)

    except Exception as error:
        # Обработка непредвиденных ошибок
        error_msg = str(error)
        print(f"ls: {error_msg}")
        log_command(f"ls {'-l' if detailed else ''} {path}", success=False, error_msg=error_msg)