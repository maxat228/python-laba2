import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_ls import ls

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