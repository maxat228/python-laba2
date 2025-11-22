import os
from unittest.mock import patch, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from command_cat import cat

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
