import os
from datetime import datetime

# Функции для логирования
def setup_logging():
    global log_file
    log_file = "shell.log"  # Устанавливаем имя файла для логов
    if os.path.exists(log_file):  # Если файл уже существует
        open(log_file, 'w').close()  # Очищаем его содержимое

def log_command(command, success=True, error_msg=""):
    # Получаем текущее время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Открываем файл лога в режиме добавления
    with open(log_file, "a", encoding="utf-8") as log:
        if success:
            # Записываем успешную команду с временной меткой
            log.write(f"[{timestamp}] {command}\n")
        else:
            # Записываем ошибку с временной меткой
            log.write(f"[{timestamp}] ERROR: {error_msg}\n")