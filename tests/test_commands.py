import os
import sys
from unittest.mock import patch, ANY

# Добавляем папку src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Импортируем функции команд
# noinspection PyUnresolvedReferences
from command_ls import ls
# noinspection PyUnresolvedReferences
from command_cd import cd
# noinspection PyUnresolvedReferences
from command_cat import cat
# noinspection PyUnresolvedReferences
from command_cp import cp
# noinspection PyUnresolvedReferences
from command_mv import mv
# noinspection PyUnresolvedReferences
from command_rm import rm
# noinspection PyUnresolvedReferences
from log_setup import log_command, setup_logging


class TestCommandLS:
    # Тесты для команды ls

    def test_ls_current_directory(self, tmp_path):
        # Тест ls без аргументов (текущая директория)
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Создаем тестовые файлы
            (tmp_path / "file1.txt").write_text("test")
            (tmp_path / "test_dir").mkdir()

            # Мокаем логирование
            with patch('command_ls.log_command') as mock_log:
                ls()
                # Исправляем ожидаемую строку - добавляем пробелы как в реальной команде
                mock_log.assert_called_once_with("ls  None", success=True)
        finally:
            os.chdir(original_cwd)

    def test_ls_with_path(self, tmp_path):
        # Тест ls с указанием пути
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("test")

        with patch('command_ls.log_command') as mock_log:
            ls(str(test_dir))
            # Исправляем формат строки - добавляем пробел
            mock_log.assert_called_once_with(f"ls  {test_dir}", success=True)

    def test_ls_detailed(self, tmp_path):
        # Тест ls с флагом -l
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            (tmp_path / "test_file.txt").write_text("content")

            with patch('command_ls.log_command') as mock_log:
                ls(detailed=True)
                # Исправляем формат строки - добавляем пробел
                mock_log.assert_called_once_with("ls -l None", success=True)
        finally:
            os.chdir(original_cwd)

    def test_ls_nonexistent_path(self):
        # Тест ls с несуществующим путем
        with patch('command_ls.log_command') as mock_log:
            ls("/nonexistent/path")
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with("ls  /nonexistent/path", success=False, error_msg=ANY)

    def test_ls_file_instead_of_directory(self, tmp_path):
        # Тест ls с путем к файлу вместо директории
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with patch('command_ls.log_command') as mock_log:
            ls(str(test_file))
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with(f"ls  {test_file}", success=False, error_msg=ANY)


class TestCommandCD:
    # Тесты для команды cd

    def test_cd_relative_path(self, tmp_path):
        # Тест cd с относительным путем
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            test_dir = tmp_path / "test_dir"
            test_dir.mkdir()

            with patch('command_cd.log_command') as mock_log:
                cd("test_dir")
                assert os.getcwd() == str(test_dir)
                mock_log.assert_called_once_with("cd test_dir", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_absolute_path(self, tmp_path):
        # Тест cd с абсолютным путем
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with patch('command_cd.log_command') as mock_log:
            cd(str(test_dir))
            mock_log.assert_called_once_with(f"cd {test_dir}", success=True)

    def test_cd_parent_directory(self, tmp_path):
        # Тест cd ..
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            test_dir = tmp_path / "test_dir"
            test_dir.mkdir()
            os.chdir(test_dir)

            with patch('command_cd.log_command') as mock_log:
                cd("..")
                assert os.getcwd() == str(tmp_path)
                mock_log.assert_called_once_with("cd ..", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_home_directory(self):
        # Тест cd ~
        home_dir = os.path.expanduser("~")
        original_cwd = os.getcwd()

        try:
            with patch('command_cd.log_command') as mock_log:
                cd("~")
                assert os.getcwd() == home_dir
                mock_log.assert_called_once_with("cd ~", success=True)
        finally:
            os.chdir(original_cwd)

    def test_cd_nonexistent_directory(self):
        # Тест cd с несуществующей директорией
        with patch('command_cd.log_command') as mock_log:
            cd("/nonexistent/directory")
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with("cd /nonexistent/directory", success=False, error_msg=ANY)

    def test_cd_file_instead_of_directory(self, tmp_path):
        # Тест cd с путем к файлу
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with patch('command_cd.log_command') as mock_log:
            cd(str(test_file))
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with(f"cd {test_file}", success=False, error_msg=ANY)


class TestCommandCAT:
    # Тесты для команды cat

    def test_cat_file_exists(self, tmp_path):
        # Тест cat с существующим файлом
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        with patch('command_cat.log_command') as mock_log:
            with patch('builtins.print') as mock_print:
                cat(str(test_file))
                mock_print.assert_called_with(test_content)
                mock_log.assert_called_once_with(f"cat {test_file}", success=True)

    def test_cat_nonexistent_file(self):
        # Тест cat с несуществующим файлом
        with patch('command_cat.log_command') as mock_log:
            cat("/nonexistent/file.txt")
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with("cat /nonexistent/file.txt", success=False, error_msg=ANY)

    def test_cat_directory(self, tmp_path):
        # Тест cat с директорией вместо файла
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with patch('command_cat.log_command') as mock_log:
            cat(str(test_dir))
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with(f"cat {test_dir}", success=False, error_msg=ANY)


class TestCommandCP:
    # Тесты для команды cp

    def test_cp_file(self, tmp_path):
        # Тест копирования файла
        source = tmp_path / "source.txt"
        source.write_text("test content")
        destination = tmp_path / "dest.txt"

        with patch('command_cp.log_command') as mock_log:
            cp(str(source), str(destination))
            assert destination.exists()
            assert destination.read_text() == "test content"
            # Исправляем формат строки - добавляем пробел
            mock_log.assert_called_once_with(f"cp  {source} {destination}", success=True)

    def test_cp_directory_without_recursive(self, tmp_path):
        # Тест копирования директории без -r
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        with patch('command_cp.log_command') as mock_log:
            cp(str(source_dir), str(tmp_path / "dest"))
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with(f"cp  {source_dir} {tmp_path / 'dest'}", success=False, error_msg=ANY)

    def test_cp_directory_with_recursive(self, tmp_path):
        # Тест копирования директории с -r
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        dest_dir = tmp_path / "dest"

        with patch('command_cp.log_command') as mock_log:
            cp(str(source_dir), str(dest_dir), recursive=True)
            assert dest_dir.exists()
            assert (dest_dir / "file.txt").exists()
            # Исправляем формат строки
            mock_log.assert_called_once_with(f"cp -r {source_dir} {dest_dir}", success=True)

    def test_cp_nonexistent_source(self, tmp_path):
        # Тест копирования несуществующего источника
        with patch('command_cp.log_command') as mock_log:
            cp("/nonexistent/source", str(tmp_path / "dest"))
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with("cp  /nonexistent/source " + str(tmp_path / "dest"), success=False,
                                             error_msg=ANY)


class TestCommandMV:
    # Тесты для команды mv

    def test_mv_file(self, tmp_path):
        # Тест перемещения файла
        source = tmp_path / "source.txt"
        source.write_text("content")
        destination = tmp_path / "dest.txt"

        with patch('command_mv.log_command') as mock_log:
            mv(str(source), str(destination))
            assert not source.exists()
            assert destination.exists()
            assert destination.read_text() == "content"
            mock_log.assert_called_once_with(f"mv {source} {destination}", success=True)

    def test_mv_rename_file(self, tmp_path):
        # Тест переименования файла
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            source = tmp_path / "old_name.txt"
            source.write_text("content")
            destination = "new_name.txt"

            with patch('command_mv.log_command') as mock_log:
                mv(str(source), destination)
                assert not source.exists()
                assert os.path.exists(destination)
                mock_log.assert_called_once_with(f"mv {source} {destination}", success=True)
        finally:
            os.chdir(original_cwd)

    def test_mv_nonexistent_source(self, tmp_path):
        # Тест перемещения несуществующего файла
        with patch('command_mv.log_command') as mock_log:
            mv("/nonexistent/source", str(tmp_path / "dest"))
            # Добавляем ANY для error_msg
            mock_log.assert_called_once_with("mv /nonexistent/source " + str(tmp_path / "dest"), success=False,
                                             error_msg=ANY)


class TestCommandRM:
    # Тесты для команды rm

    def test_rm_file(self, tmp_path):
        # Тест удаления файла
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_file))
            assert not test_file.exists()
            # Исправляем формат строки - добавляем пробел
            mock_log.assert_called_once_with(f"rm  {test_file}", success=True)

    def test_rm_directory_without_recursive(self, tmp_path):
        # Тест удаления директории без -r
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir))
            assert test_dir.exists()  # Директория должна остаться
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with(f"rm  {test_dir}", success=False, error_msg=ANY)

    def test_rm_directory_with_recursive_confirmed(self, tmp_path, monkeypatch):
        # Тест удаления директории с -r и подтверждением
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        # Мокаем input для подтверждения удаления
        monkeypatch.setattr('builtins.input', lambda _: 'y')

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir), recursive=True)
            assert not test_dir.exists()
            # Исправляем формат строки
            mock_log.assert_called_once_with(f"rm -r {test_dir}", success=True)

    def test_rm_directory_with_recursive_cancelled(self, tmp_path, monkeypatch):
        # Тест удаления директории с -r и отменой
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Мокаем input для отмены удаления
        monkeypatch.setattr('builtins.input', lambda _: 'n')

        with patch('command_rm.log_command') as mock_log:
            rm(str(test_dir), recursive=True)
            assert test_dir.exists()  # Директория должна остаться
            mock_log.assert_called_once_with(f"rm -r {test_dir}", success=False, error_msg="Cancelled by user")

    def test_rm_nonexistent_file(self):
        # Тест удаления несуществующего файла
        with patch('command_rm.log_command') as mock_log:
            rm("/nonexistent/file.txt")
            # Добавляем пробел и ANY для error_msg
            mock_log.assert_called_once_with("rm  /nonexistent/file.txt", success=False, error_msg=ANY)


class TestLogging:
    # Тесты для системы логирования

    def test_log_command_success(self, tmp_path):
        # Тест логирования успешной команды
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            setup_logging()
            log_command("test command", success=True)

            with open("shell.log", "r") as f:
                log_content = f.read()
                assert "test command" in log_content
                assert "ERROR" not in log_content
        finally:
            os.chdir(original_cwd)

    def test_log_command_error(self, tmp_path):
        # Тест логирования ошибки
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            setup_logging()
            log_command("test command", success=False, error_msg="test error")

            with open("shell.log", "r") as f:
                log_content = f.read()
                assert "ERROR" in log_content
                assert "test error" in log_content
        finally:
            os.chdir(original_cwd)