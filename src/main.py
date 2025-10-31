import os, shutil, stat, time
from datetime import datetime

# Функции для логирования

# Настройка файла лога
def setup_logging():
    # Настройка файла лога
    global log_file
    log_file = "shell.log"
    # Проверка на существование файла
    if os.path.exists(log_file):
        open(log_file, 'w').close()

# Запись команды в лог с временной меткой
def log_command(command, success=True, error_msg=""):
    # Получаем текущее время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Открываем файл лога в режиме append
    with open(log_file, "a", encoding="utf-8") as log:
        # Проверяем, была ли ошибка, и записываем либо команду, либо сообщение об ошибке
        if success:
            log.write(f"[{timestamp}] {command}\n")
        else:
            log.write(f"[{timestamp}] ERROR: {error_msg}\n")

# Команда ls - отображение файлов и каталогов
def ls(path=None, detailed=False):
    try:
        # Если путь не указан, используем текущую директорию
        if path is None:
            # Текущая директория
            target_path = '.'
        else:
            target_path = path

        # Преобразование пути в абсолютный путь
        abs_path = os.path.abspath(target_path)

        # Проверяем существует ли указанный путь
        if not os.path.exists(abs_path):
            error_msg = f"No such file or directory: '{path}'"
            print(f"ls: {error_msg}")
            # Логируем неудачную команду
            log_command(f"ls {'-l' if detailed else ''}{path}", success=False, error_msg=error_msg)
            return

        if not os.path.isdir(abs_path):
            error_msg = f"'{path}' is not a directory'"
            print(f"ls: {error_msg}")
            log_command(f"ls {'-l ' if detailed else ''}{path}", success=False, error_msg=error_msg)
            return

        # Получаем список всех файлов и папок в указанной директории
        items = os.listdir(abs_path)

        # Если запрошен подробный вывод
        if detailed:
            # Проходка по всем отсортированным элементам
            for element in sorted(items):
                # Полный путь к элементу
                item_path = os.path.join(abs_path, element)
                try:
                    # Получаем информацию о файле/папке (размер, права, время и прочее)
                    stat_info = os.stat(item_path)

                    # Определяем тип элемента: папка, файл или ссылка
                    if stat.S_ISDIR(stat_info.st_mode):
                        file_type = "d" # папка
                    elif stat.S_ISLINK(stat_info.st_mode):
                        file_type = "l" # ссылка
                    else:
                        file_type = "-" # обычный файл

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

                    # размер файла в байтах
                    size = stat_info.st_size
                    # Преобразуем время изменения в читаемый формат
                    modified_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime(stat_info.st_mtime))

                    # Выводим отформатированную информацию
                    print(f"{file_type}{perm} {size:>8} {modified_time} {element}")

                except OSError:
                    # Если не удалось получить информацию об элементе
                    print(f"?????????? ?         ????-??-?? ??:?? {element}")
        else:
            # Простой вывод с именами
            for element in sorted(items):
                item_path = os.path.join(abs_path, element)
                # Для папок добавляем / в конце
                if os.path.isdir(item_path):
                    print(f"{element}/")
                else:
                    print(f"{element}")

        # Логируем успешное выполнение команды
        log_command(f"ls {'-l ' if detailed else ''}{path}", success=True)

    except Exception as error:
        # Обработка непредвиденных ошибок
        error_msg = str(error)
        print(f"ls: {error_msg}")
        log_command(f"ls {'-l ' if detailed else ''}{path}", success=False, error_msg=error_msg)

# Команда cd - смена текущей рабочей директории
def cd(path):
    try:
        # Обработка случаев
        if path == "..":
            # Переход на уровень выше - получаем родительскую директорию
            new_path = os.path.dirname(os.getcwd())
        elif path == "~":
            # Переход в домашнюю директорию пользователя
            new_path = os.path.expanduser("~")
        else:
            # Обычный путь преобразуем в абсолютный
            new_path = os.path.abspath(path)

        # Проверяем существование целевой директории
        if not os.path.exists(new_path):
            error_msg = f"No such file or directory: '{path}'"
            print(f"cd: {error_msg}")
            log_command(f"cd {path}", success=False, error_msg=error_msg)
            return

        # Проверяем, что это действительно директория
        if not os.path.isdir(new_path):
            error_msg = f"'{path}' is not a directory"
            print(f"cd: {error_msg}")
            log_command(f"cd {path}", success=False, error_msg=error_msg)
            return

        # Смена директории
        os.chdir(new_path)
        log_command(f"cd {path}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"cd: {error_msg}")
        log_command(f"cd {path}", success=False, error_msg=error_msg)

# Команда cat - вывод содержимого файла в консоль
def cat(file_path):
    try:
        abs_file_path = os.path.abspath(file_path)

        if os.path.exists(abs_file_path):
            error_msg = f"No such file or directory: '{file_path}'"
            print(f"cat: {error_msg}")
            log_command(f"cat {file_path}", success=False, error_msg=error_msg)
            return

        if os.path.isdir(abs_file_path):
            error_msg = f"'{file_path}' is a directory"
            print(f"cat: {error_msg}")
            log_command(f"cat {file_path}", success=False, error_msg=error_msg)
            return

        # Открываем файл в режиме чтения и выводим содержимое в консоль
        with open(abs_file_path, "r", encoding="utf-8") as file:
            print(file.read())

        log_command(f"cat {file_path}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"cat: {error_msg}")
        log_command(f"cat {file_path}", success=False, error_msg=error_msg)

# Команда CP - копирование файлов и папок
def cp(source, destination, recursive=False):
    try:
        # Преобразуем оба пути в абсолютные
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)

        # Проверяем существование источника
        if not os.path.exists(abs_source):
            error_msg = f"No such file or directory: '{source}'"
            print(f"cp: {error_msg}")
            log_command(f"cp {'-r ' if recursive else ''}{source} {destination}",
                        success=False, error_msg=error_msg)
            return

        # Если источник - папка, но не указан флаг -r, выдаем ошибку
        if os.path.isdir(abs_source) and not recursive:
            error_msg = f"'{source}' is a directory (not copied)"
            print(f"cp: {error_msg}")
            log_command(f"cp {'-r ' if recursive else ''}{source} {destination}",
                        success=False, error_msg=error_msg)
            return

        # Выполняем копирование в зависимости от типа источника
        if os.path.isdir(abs_source):
            # Рекурсивное копирование папки со всем содержимым
            shutil.copytree(abs_source, abs_dest)
        else:
            # Копирование одиночного файла
            shutil.copy2(abs_source, abs_dest)

        log_command(f"cp {'-r ' if recursive else ''}{source} {destination}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"cp: {error_msg}")
        log_command(f"cp {'-r ' if recursive else ''}{source} {destination}", success=False,
                    error_msg=error_msg)

# Команда mv - перемещение или переименовывание файлов/папок
def mv(source, destination):
    try:
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)

        if not os.path.exists(abs_source):
            error_msg = f"No such file or directory: '{source}'"
            print(f"mv: {error_msg}")
            log_command(f"mv {source} {destination}", success=False, error_msg=error_msg)
            return

        # Выполняем перемещение/переименование
        shutil.move(abs_source, abs_dest)
        log_command(f"mv {source} {destination}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"mv: {error_msg}")
        log_command(f"mv {source} {destination}", success=False, error_msg=error_msg)

# Команда rm - удаление файлов и папок
def rm(target, recursive=False):
    try:
        target_abs = os.path.abspath(target)

        # Защита от случайного удаления важных директорий
        if target_abs in ['/', os.path.dirname(target_abs)]:
            error_msg = "Cannot remove root or parent directory"
            print(f"rm: {error_msg}")
            log_command(f"rm {'-r ' if recursive else ''}{target}", success=False, error_msg=error_msg)
            return

        # Проверяем существование цели
        if not os.path.exists(target_abs):
            error_msg = f"No such file or directory: '{target}'"
            print(f"rm: {error_msg}")
            log_command(f"rm {'-r ' if recursive else ''}{target}", success=False, error_msg=error_msg)
            return

        # Обработка удаления папки
        if os.path.isdir(target_abs):
            if not recursive:
                error_msg = f"'{target}' is a directory"
                print(f"rm: {error_msg}")
                log_command(f"rm {'-r ' if recursive else ''}{target}", success=False, error_msg=error_msg)
                return

            # Запрашиваем подтверждение для удаления папки
            confirm = input(f"rm: Do you want to remove '{target}'? [y/N] ")
            if confirm.lower() != 'y':
                print("rm: cancellation confirmed")
                log_command(f"rm {'-r ' if recursive else ''}{target}", success=False,
                            error_msg="Cancelled by user")
                return

            # Рекурсивно удаляем папку со всем содержимым
            shutil.rmtree(target_abs)
        else:
            # Удаляем одиночный файл
            os.remove(target_abs)

        log_command(f"rm {'-r ' if recursive else ''}{target}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"rm: {error_msg}")
        log_command(f"rm {'-r ' if recursive else ''}{target}", success=False, error_msg=error_msg)

# Парсинг введенной пользователем команды
def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []

    command, args = parts[0], parts[1:]
    return command, args


