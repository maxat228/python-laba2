import os, shutil
from log_setup import log_command

# Команда rm - удаление файлов и папок
def rm(target, recursive=False):
    try:
        target_abs = os.path.abspath(target)

        # Защита от случайного удаления важных директорий
        if target_abs in ['/', os.path.dirname(target_abs)]:
            error_msg = "Cannot remove root or parent directory"
            print(f"rm: {error_msg}")
            log_command(f"rm {'-r' if recursive else ''} {target}", success=False, error_msg=error_msg)
            return

        if not os.path.exists(target_abs):
            error_msg = f"No such file or directory: '{target}'"
            print(f"rm: {error_msg}")
            log_command(f"rm {'-r' if recursive else ''} {target}", success=False, error_msg=error_msg)
            return

        # Обработка удаления папки
        if os.path.isdir(target_abs):
            if not recursive:
                # Если не указан флаг -r для удаления директории
                error_msg = f"'{target}' is a directory"
                print(f"rm: {error_msg}")
                log_command(f"rm {'-r' if recursive else ''} {target}", success=False, error_msg=error_msg)
                return

            # Запрашиваем подтверждение для удаления папки (опасная операция)
            confirm = input(f"rm: Do you want to remove '{target}'? [y/N] ")
            if confirm.lower() == 'N':
                # Пользователь отменил удаление
                print("rm: cancellation confirmed")
                log_command(f"rm {'-r' if recursive else ''} {target}", success=False, error_msg="Cancelled by user")
                return

            shutil.rmtree(target_abs)
        else:
            os.remove(target_abs)

        log_command(f"rm {'-r' if recursive else ''} {target}", success=True)

    except Exception as error:
        error_msg = str(error)
        print(f"rm: {error_msg}")
        log_command(f"rm {'-r' if recursive else ''} {target}", success=False, error_msg=error_msg)